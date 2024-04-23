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
    #return HttpResponse("Hello World!")

def upload_fileDes(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():

            dataFrame = pd.read_csv(request.FILES['file'].temporary_file_path(), index_col=None)

            data_set = DataSet.objects.create(name="datasetStatistics")
            

            for col in dataFrame.columns:
                mean=st.mean(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="mean",value=mean,data_set=data_set)

            for col in dataFrame.columns:
                mean=st.median(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="median",value=mean,data_set=data_set)

            for col in dataFrame.columns:
                mean=st.mode(dataFrame[col].dropna().values)
                Statistic.objects.create(col_name=col,stat_name="mode",value=mean,data_set=data_set)

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


            Nan_Val = False

            for col in data.columns:
                index = 0
                for value in data[col]:

                    if value is None or pd.isna(value) or pd.isnull(value):
                        Nan_Val = True
                        output = f"Bad data try again. {col} on {index}"
                        model = {"dataTableHTML": output}
                        return render(request, "base.html", model)  
                    index += 1


            first_column_length = len(data[data.columns[0]])
            all_same_length = True

            for col in data.columns:
                if len(data[col]) != first_column_length:
                    all_same_length = False
                    output = f"Bad Data Please Try Again! \n {col}"
                    model = {"dataTableHTML": output}
                    return render(request, "base.html", model) 

            if all_same_length==False or len(col_names)<2 or Nan_Val==True: 
                output = "Bad Data Please Try Again!"
                model = {"dataTableHTML": output}
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
                'Y-name': Y_col_name,
                'X-names': X_cols_names,
                'coefficients_with_names': coefficients_with_names
            }

            return render(request, "regression.html", model)

              