# data_analysis_app/views.py
from distutils.errors import PreprocessError
import filecmp
import logging
import os
import profile
from django.shortcuts import render, HttpResponse
from sklearn import preprocessing
from sklearn.compose import ColumnTransformer
from data_analysis_project import settings
import pandas as pd
from ydata_profiling import ProfileReport
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO
import base64
from io import StringIO
import pickle

def data_tab(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv")
 # Get the first ten rows of the dataset
    df_first_ten = df.head(10)
    df_last_ten = df.tail(10)

    # Get information about the columns (data types, non-null counts, null counts)
    columns_info = pd.DataFrame({
        'Column Name': df.columns,
        'Data Type': df.dtypes,
        'Non-Null Count': df.notnull().sum(),
        'Null Count': df.isnull().sum()
    })

    # Convert DataFrame to HTML for rendering in template
    table_html1 = df_first_ten.to_html(classes='table table-hover table-bordered')
    table_html2 = df_last_ten.to_html(classes='table table-hover table-bordered')

    # Include the columns information in the HTML template
    columns_info_html = f"{columns_info.to_html(classes='table table-hover table-bordered', index=False)}"

    return render(request, 'data_tab.html', {'table_html1': table_html1, 'table_html2':table_html2, 'columns_info_html': columns_info_html})



def profile_view(request):
    df = pd.read_csv("C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv")

    # Create a profile report
    #profile = ProfileReport(df, title="Pandas Profiling Report")
    
    #print('Setting Dir Path')
    #print(settings.TEMPLATE_DIR)
    templates_dir = settings.TEMPLATE_DIR
    report_path = os.path.join(templates_dir, 'report.html')

    # # Save the report to the templates directory
    profile.to_file(report_path)
    # Pass the HTML file path to the template

    return render(request, 'report.html', {'report_path': report_path})


  
def descriptive_statistics_tab(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv")
    
    # Perform descriptive statistics using pandas
    descriptive_stats = df.describe().to_html(classes='table table-bordered table-hover')

    return render(request, 'descriptive_statistics_tab.html', {'descriptive_stats': descriptive_stats})




def box_plot(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv")

    # Default settings for the plot
    default_category = 'Pclass'
    default_value = 'Fare'

    # Get user-selected options (if any)
    selected_category = request.GET.get('category', default_category)
    selected_value = request.GET.get('value', default_value)

    # Validate selected features
    if selected_category not in df.columns or selected_value not in df.columns:
        error_message = "Invalid features selected for box plot."
        return render(request, 'error_page.html', {'error_message': error_message})

    # Create an interactive box plot using Plotly
    fig = px.box(df, x=selected_category, y=selected_value, title=f'Box Plot: {selected_value} by {selected_category}')

    # Convert the plot to HTML for rendering in the template
    plot_html = fig.to_html(full_html=False)

    # Pass parameters to the template for customization options
    box_cus_options = {
        'categories': df.columns.tolist(),
        'default_category': default_category,
        'default_value': default_value,
        'selected_category': selected_category,
        'selected_value': selected_value,
    }
    return {'plot_html': plot_html, 'box_cus_options': box_cus_options}
    #return render(request, 'box_plot.html', {'plot_html': plot_html, 'customization_options': customization_options})








import pandas as pd
import plotly.express as px
from django.shortcuts import render

def exploratory_data_analysis_tab(request):
    # Read flight dataset from CSV
    df = pd.read_csv("C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv")

    # Default settings for the plot
    default_feature = 'duration'
    default_bins = 20

    # Get user-selected options (if any)
    selected_feature = request.GET.get('feature', default_feature)
    selected_bins = int(request.GET.get('bins', default_bins))

    # Create an interactive histogram using Plotly
    fig = px.histogram(df, x=selected_feature, nbins=selected_bins, title=f'{selected_feature} Distribution')

    # Convert the plot to HTML for rendering in the template
    plot_html = fig.to_html(full_html=False)

    # Pass parameters to the template for customization options
    customization_options = {
        'features': df.columns.tolist(),
        'default_feature': default_feature,
        'default_bins': default_bins,
        'selected_feature': selected_feature,
        'selected_bins': selected_bins,
    }

    ##########################   Box Plot ##############################
    # Default settings for the plot
    default_category = 'airline'
    default_value = 'duration'

    # Get user-selected options (if any)
    selected_category = request.GET.get('category', default_category)
    selected_value = request.GET.get('value', default_value)

    # Validate selected features
    if selected_category not in df.columns or selected_value not in df.columns:
        error_message = "Invalid features selected for box plot."
        return render(request, 'error_page.html', {'error_message': error_message})

    # Create an interactive box plot using Plotly
    fig = px.box(df, x=selected_category, y=selected_value, title=f'Box Plot: {selected_value} by {selected_category}')

    # Convert the plot to HTML for rendering in the template
    box_plot_html = fig.to_html(full_html=False)

    # Pass parameters to the template for customization options
    box_cus_options = {
        'categories': df.columns.tolist(),
        'default_category': default_category,
        'default_value': default_value,
        'selected_category': selected_category,
        'selected_value': selected_value,
    }

    ####################### Scatter Plot ###############################
    # Default settings for the scatter plot
    default_x_feature = 'duration'
    default_y_feature = 'price'

    # Get user-selected options (if any)
    selected_x_feature = request.GET.get('x_feature', default_x_feature)
    selected_y_feature = request.GET.get('y_feature', default_y_feature)

    # Create an interactive scatter plot using Plotly
    fig_scatter = px.scatter(df, x=selected_x_feature, y=selected_y_feature, color='class',
                             title=f'Scatter Plot: {selected_x_feature} vs. {selected_y_feature}')

    # Convert the scatter plot to HTML for rendering in the template
    plot_html_scatter = fig_scatter.to_html(full_html=False)

    # Pass parameters to the template for customization options
    customization_options_scatter = {
        'features': df.columns.tolist(),
        'default_x_feature': default_x_feature,
        'default_y_feature': default_y_feature,
        'selected_x_feature': selected_x_feature,
        'selected_y_feature': selected_y_feature,
    }

    ################################ Pie Chart #################################
    # Default settings for the pie chart
    default_feature_pie = 'class'

    # Get user-selected options (if any)
    selected_feature_pie = request.GET.get('feature_pie', default_feature_pie)

    # Create an interactive pie chart using Plotly
    fig_pie = px.pie(df, names=selected_feature_pie, title=f'Pie Chart: {selected_feature_pie}')

    # Convert the pie chart to HTML for rendering in the template
    plot_html_pie = fig_pie.to_html(full_html=False)

    # Pass parameters to the template for customization options
    customization_options_pie = {
        'features_pie': df.columns.tolist(),
        'default_feature_pie': default_feature_pie,
        'selected_feature_pie': selected_feature_pie,
    }

    return render(request, 'exploratory_data_analysis_tab.html', {
        'plot_html': plot_html,
        'customization_options': customization_options,
        'box_plot_html': box_plot_html,
        'box_cus_options': box_cus_options,
        'plot_html_scatter': plot_html_scatter,
        'customization_options_scatter': customization_options_scatter,
        'plot_html_pie': plot_html_pie,
        'customization_options_pie': customization_options_pie,
    })













def export_to_csv(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv")

    # Generate CSV file
    csv_file = df.to_csv(index=False)

    # Create HTTP response with CSV file
    response = HttpResponse(csv_file, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="titanic_data.csv"'
    
    return response


def export_to_excel(request):
    # Read Titanic dataset from CSV
    df = pd.read_csv("C:\\Users\\moksh\\Downloads\\cleaned_flight_data (1).csv")

    # Generate Excel file
    excel_file = BytesIO()
    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    excel_file.seek(0)

    # Create HTTP response with Excel file
    response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="titanic_data.xlsx"'

    return response




from django.shortcuts import render
import os
import pandas as pd
import pickle
from sklearn.pipeline import Pipeline

def predict_flight_price(request):
    if request.method == 'POST':
        try:
            # Load the trained model from the pickle file
            model_filename = 'flight_price_model.pkl'
            model_path = os.path.join(os.path.dirname(__file__), 'models', model_filename)

            with open(model_path, 'rb') as model_file:
                # Try to load the model as a pipeline
                try:
                    model = pickle.load(model_file)
                    # Extract the actual model from the pipeline if it's there
                    if isinstance(model, Pipeline):
                        model = model.named_steps['regressor']
                except AttributeError:
                    # If not a pipeline, load it directly
                    model = pickle.load(model_file)

            # Get user input from the form
            duration = float(request.POST.get('duration'))
            days_left = float(request.POST.get('days_left'))
            time_of_day = float(request.POST.get('time_of_day'))

            # Convert to DataFrame and dummy encode categorical variables
            input_data = pd.DataFrame({
                'duration': [duration],
                'days_left': [days_left],
                'time_of_day': [time_of_day],
            })

            # Make prediction
            prediction = model.predict(input_data)[0]

            # Render the result
            return render(request, 'prediction_result.html', {'prediction': prediction})

        except Exception as e:
            # Handle exceptions
            return render(request, 'flight_price_prediction_form.html', {'prediction': None, 'error': str(e)})

    # If the form is not submitted, render the empty form
    return render(request, 'predict_survival.html', {'prediction': None})

