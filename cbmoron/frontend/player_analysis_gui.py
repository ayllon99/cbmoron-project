from taipy.gui import Gui
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
import numpy as np


data = pd.DataFrame({
    'City': np.random.choice(["Bangkok", "Chiang Mai", "Vientiane", "Luang Prabang", "Yangon", "Naypyitaw"], size=10),
    'Month_Year': np.random.choice(["2020-01", "2020-02", "2020-03", "2020-04", "2020-05", "2020-06"], size=10),
    'Gender': np.random.choice(["Male", "Female"], size=10),
    'Customer_type': np.random.choice(["Walk-in", "Online"], size=10),
    'Total': np.random.randint(1, 100, size=10)
})

def create_perc_fig(df, group_column):
    # Group, sum, and convert to percentage
    df = df.groupby(['Month_Year', group_column])['Total'].sum().unstack(fill_value=0)
    df = df.div(df.sum(axis=1), axis=0).reset_index().melt(id_vars='Month_Year', var_name=group_column, value_name='Percentage')
    df['Percentage'] = (df.loc[:, 'Percentage'].round(3) * 100)
    
    # Create and return the plot
    fig = px.bar(df, x='Month_Year', y='Percentage', color=group_column, title=f"Evolution of Sales by {group_column} over Time", labels={'Percentage': '% of Total'}, text_auto=True)
    return fig



city = ["Bangkok", "Chiang Mai", "Vientiane", "Luang Prabang", "Yangon", "Naypyitaw"]

filtered_data = data.loc[
    data["City"].isin(city)
]

fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')


def on_selector(state):
    filtered_data = state.data.loc[
        state.data["City"].isin(state.city)
    ]

    
    state.fig_gender_perc = create_perc_fig(filtered_data, 'Gender')
    state.fig_customer_type_perc = create_perc_fig(filtered_data, 'Customer_type')




with tgb.Page() as page:
    tgb.text("Sales Insights", class_name="h1")

    tgb.text("Analysis", class_name="h2")

    tgb.selector(value="{city}", lov=["Bangkok", "Chiang Mai", "Vientiane", "Luang Prabang", "Yangon", "Naypyitaw"],
                 dropdown=True,
                 multiple=True,
                 label="Select cities",
                 class_name="fullwidth",
                 on_change=on_selector)

    with tgb.layout("1 1"):
        tgb.chart(figure="{fig_gender_perc}")
        tgb.chart(figure="{fig_customer_type_perc}")

    tgb.table("{data}")


if __name__ == "__main__":
    gui = Gui(page)
    gui.run(title="Sales", port=2452)
    
