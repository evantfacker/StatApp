from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.urls import reverse
from .forms import UploadFileForm
import pandas as pd
from django_pandas.io import read_frame
import statistics as st
from django.db.models import Avg
from sklearn.linear_model import LinearRegression
from .models import DataSet, Statistic
import numpy as np



# Create your views here.
def home(request):
    return render(request, "base.html")

def upload_fileDes(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            dataFrame = pd.read_csv(request.FILES['file'].temporary_file_path(), index_col=None)

            ## Error Traping

            for col in dataFrame.columns:
                try:
                    pd.to_numeric(dataFrame[col])  # Try to convert column to numeric
                    pass
                except ValueError:
                    output = f"Bad data try again. Non-Numeric Data in column: '{col}'"
                    model = {"BadDataAlertHTML_Des": output,
                             "BadDataAlertHTML": ""}
                    return render(request, "base.html", model)

            data_set = DataSet.objects.create(name="datasetStatistics")
            

            for col in dataFrame.columns:
                mean=st.mean(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="mean",value=mean,data_set=data_set)

            for col in dataFrame.columns:
                median=st.median(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="median",value=median,data_set=data_set)

            for col in dataFrame.columns:
                try:
                    data=dataFrame[col].dropna().values
                    mode=st.mode(data)
                    if mode==data[0]:
                        Statistic.objects.create(col_name=col,stat_name="mode",value=0,data_set=data_set)
                    else:
                        Statistic.objects.create(col_name=col,stat_name="mode",value=mode,data_set=data_set)
                except st.StatisticsError:
                        Statistic.objects.create(col_name=col,stat_name="mode",value=0,data_set=data_set)


            for col in dataFrame.columns:
                mean=min(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="min",value=mean,data_set=data_set)

            for col in dataFrame.columns:
                mean=max(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="max",value=mean,data_set=data_set)

            for col in dataFrame.columns:
                mean=st.variance(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="variance",value=mean,data_set=data_set)

            for col in dataFrame.columns:
                mean=st.stdev(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="sDev",value=mean,data_set=data_set)

            return redirect(reverse('view_dataset', kwargs={'dataset_id': data_set.id}))         
 

def view_dataset(request, dataset_id):
    dataset = get_object_or_404(DataSet, pk=dataset_id)
    statistics = convert_to_dict(list(dataset.statistics.all()))

    model = {
        'dataset_name': dataset.name,
        'statistics': statistics
    }

    return render(request, "descriptivestatistics.html", model)


def convert_to_dict(statistics):
    result = {}
    for stat in statistics:
        if stat.col_name not in result:
            result[stat.col_name] = {}
        result[stat.col_name][stat.stat_name] = stat.value
    return result


def upload_fileReg(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            data = pd.read_csv(request.FILES['file'].temporary_file_path())

            col_names = []

            for col in data.columns:
                col_names.append(str(col))

            ## Error Trapping

            first_column_length = len(data[data.columns[0]].dropna().values)
            all_same_length = True

            for col in data.columns:
                if len(data[col].dropna().values) != first_column_length:
                    all_same_length = False
                    output = f"Bad Data Please Try Again! <br> Column '{col}' is an unacceptable length."
                    model = {"BadDataAlertHTML": output,
                             "BadDataAlertHTML_Des": ""}
                    return render(request, "base.html", model) 



            Nan_Val = False

            for col in data.columns:
                index = 0
                for value in data[col]:


                    if value is None or pd.isna(value) or pd.isnull(value):
                        Nan_Val = True
                        col_num = index + 2
                        output = f"Bad data try again. <br> In column: '{col}' <br> In Row: {col_num}"
                        model = {"BadDataAlertHTML": output,
                                 "BadDataAlertHTML_Des": ""}
                        return render(request, "base.html", model)  
                    index += 1
            
            for col in data.columns:
                try:
                    pd.to_numeric(data[col])  # Try to convert column to numeric
                    pass
                except ValueError:
                    output = f"Bad data try again. Non-Numeric Data in column: '{col}'"
                    model = {"BadDataAlertHTML": output,
                             "BadDataAlertHTML_Des": ""}
                    return render(request, "base.html", model)

            if all_same_length==False or len(col_names)<2 or Nan_Val==True: 
                output = "Bad Data Please Try Again! <br> Must have at least two columns of numeric data with equal length."
                model = {"BadDataAlertHTML": output,
                         "BadDataAlertHTML_Des": ""}
                return render(request, "base.html", model)


            ##Logic and Calculations

            col_names = []

            for col in data.columns:
                col_names.append(str(col))

            Y_col_name = col_names[0]

            X_cols_names = col_names[1:]

            print(X_cols_names)

            # Perform linear regression
            Regmodel = LinearRegression()
            Regmodel.fit(data[X_cols_names], data[Y_col_name])

            # Prepare data for display
            intercept = Regmodel.intercept_
            coefficients = Regmodel.coef_
            column_names = data[X_cols_names].columns.tolist()

            coefficients_with_names = zip(column_names, coefficients)

            # Pass data to template
            model = {
                'intercept': intercept,
                'coefficients': coefficients,
                'Y_col_name': Y_col_name,
                'X-names': X_cols_names,
                'coefficients_with_names': coefficients_with_names
            }

            return render(request, "regression.html", model)

              