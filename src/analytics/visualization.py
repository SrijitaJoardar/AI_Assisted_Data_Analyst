import pandas as pd
import plotly.express as px


def create_bar_chart(results: list[dict]):
    if not results or len(results) < 2:
        return None

    df = pd.DataFrame(results)

    # Identify numerical columns
    numerical_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    # Identify categorical columns
    categorical_columns = df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    # We need exactly one categorical and one numerical column
    if len(categorical_columns) != 1:
        return None

    if len(numerical_columns) != 1:
        return None

    category_column = categorical_columns[0]
    value_column = numerical_columns[0]

    fig = px.bar(
        df,
        x=category_column,
        y=value_column,
        title=f"{value_column} by {category_column}",
        text=value_column,
    )

    fig.update_layout(
        xaxis_title=category_column,
        yaxis_title=value_column,
        template="plotly_white",
        title_x=0.5,
        height=500,
    )

    fig.update_traces(
        texttemplate="%{y:,.2f}",
        textposition="outside",
        hovertemplate=(
            f"{category_column}: %{{x}}<br>"
            f"{value_column}: %{{y:,.2f}}"
            "<extra></extra>"
        ),
    )

    return fig