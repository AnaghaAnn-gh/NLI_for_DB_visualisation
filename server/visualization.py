def get_primer(df_dataset, df_name):
    # Primer function to take a dataframe and its name
    # and the name of the columns
    # and any columns with less than 20 unique values it adds the values to the primer
    # and horizontal grid lines and labeling
    primer_desc = "Use a dataframe called df with columns '" \
        + "','".join(str(x) for x in df_dataset.columns) + "'. "
    for i in df_dataset.columns:
        if len(df_dataset[i].drop_duplicates()) < 20 and df_dataset.dtypes[i] == "O":
            primer_desc = primer_desc + "\nThe column '" + i + "' has categorical values '" + \
                "','".join(str(x)
                           for x in df_dataset[i].drop_duplicates()) + "'. "
        elif df_dataset.dtypes[i] == "int64" or df_dataset.dtypes[i] == "float64":
            primer_desc = primer_desc + "\nThe column '" + i + "' is type " + \
                str(df_dataset.dtypes[i]) + " and contains numeric values. "
    primer_desc = primer_desc + "\nLabel the x and y axes appropriately."
    primer_desc = primer_desc + "\nAdd a title. Set the fig suptitle as empty."
    primer_desc = primer_desc + "{}"  # Space for additional instructions if needed
    primer_desc = primer_desc + \
        "\nUsing Python version 3.11,9, create a script using the dataframe df to graph the following: "
    pimer_code = "import pandas as pd\nimport matplotlib.pyplot as plt\n"
    pimer_code = pimer_code + "fig,ax = plt.subplots(1,1,figsize=(10,4))\n"
    pimer_code = pimer_code + \
        "ax.spines['top'].set_visible(False)\nax.spines['right'].set_visible(False) \n"
    pimer_code = pimer_code + "df=" + df_name + ".copy()\n"
    return primer_desc, pimer_code

# import plotly.express as px
# import random
# import plotly.io as pio
# import os
# def scatter(x, y):
#     fig=px.scatter(x, y, title="Scatter plot")
#     return fig

# def bar(x, y):
#     fig=px.bar(x, y, title="Bar plot")
#     return fig

# def line(x, y):
#     fig=px.line(x, y, title="Line plot")
#     return fig

# def hist(x, y):
#     fig=px.histogram(x, y, title="Histogram")
#     return fig

# def pie(x):
#     fig=px.pie(x, title="Pie chart")

# x = list(range(2023, 2073))
# y = [50 + 10 * i + random.randint(-5, 5) for i in range(50)]
# # fig = px.scatter(title='Empty Figure')

# choice=int(input("1.scatter 2.line 3.bar 4.histogram 5.pie\nEnter choice:"))
# match choice:
#     case 1: fig = scatter(x, y)
#     case 2: fig = bar(x, y)
#     case 3: fig = bar(x, y)
#     case 4: fig= hist(x, y)
#     case 5: fig=pie(x)

# path=os.path.dirname(os.path.abspath(__file__))
# path+='/images/result_graph.png'
# # fig=px.line(x, y)
# pio.write_image(fig, path)
