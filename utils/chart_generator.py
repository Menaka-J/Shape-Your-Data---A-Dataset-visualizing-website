import pandas as pd
import numpy as np
import uuid
from itertools import combinations

def generate_charts(df):
    charts = []
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    # 1. Histogram (bar chart of value counts for numeric cols)
    for col in numeric_cols:
        chart_id = str(uuid.uuid4()).replace('-', '')[:8]
        counts = df[col].dropna().value_counts().sort_index()
        try:
            config = {
                "type": "bar",
                "data": {
                    "labels": counts.index.astype(str).tolist(),
                    "datasets": [{
                        "label": f"Histogram of {col}",
                        "data": counts.tolist(),
                        "backgroundColor": "rgba(75, 200, 192, 0.6)"
                    }]
                },
                "options": {
                    "scales": {
                        "x": {"title": {"display": True, "text": col}},
                        "y": {"title": {"display": True, "text": "Count"}}
                    }
                }
            }
            charts.append({
                "id": chart_id,
                "title": f"Histogram of {col}",
                "config": config,
                "description": f"Histogram showing value counts for {col}.",
                "error": False
            })
        except Exception:
            charts.append({
                "id": chart_id,
                "title": f"Histogram of {col}",
                "config": {},
                "description": f"Could not generate histogram for {col}.",
                "error": True
            })
    
    # 2. Scatter plot for every numeric pair (x vs y)
    for i in range(len(numeric_cols)):
        for j in range(i + 1, len(numeric_cols)):
            x_col = numeric_cols[i]
            y_col = numeric_cols[j]
            chart_id = str(uuid.uuid4()).replace('-', '')[:8]
            try:
                filtered = df[[x_col, y_col]].dropna()
                data_points = [{"x": float(x), "y": float(y)} for x, y in zip(filtered[x_col], filtered[y_col])]
                config = {
                    "type": "scatter",
                    "data": {
                        "datasets": [{
                            "label": f"{x_col} vs {y_col}",
                            "data": data_points,
                            "backgroundColor": "rgba(153, 102, 255, 0.6)"
                        }]
                    },
                    "options": {
                        "scales": {
                            "x": {"title": {"display": True, "text": x_col}},
                            "y": {"title": {"display": True, "text": y_col}}
                        }
                    }
                }
                charts.append({
                    "id": chart_id,
                    "title": f"Scatter Plot: {x_col} vs {y_col}",
                    "config": config,
                    "description": f"Scatter plot showing relationship between {x_col} and {y_col}.",
                    "error": False
                })
            except Exception:
                charts.append({
                    "id": chart_id,
                    "title": f"Scatter Plot: {x_col} vs {y_col}",
                    "config": {},
                    "description": f"Could not generate scatter plot for {x_col} and {y_col}.",
                    "error": True
                })
    
    # 3. Line plot per numeric column over datetime index (if index is datetime)
    if pd.api.types.is_datetime64_any_dtype(df.index):
        for col in numeric_cols:
            chart_id = str(uuid.uuid4()).replace('-', '')[:8]
            try:
                config = {
                    "type": "line",
                    "data": {
                        "labels": df.index.astype(str).tolist(),
                        "datasets": [{
                            "label": col,
                            "data": df[col].fillna(0).tolist(),
                            "borderColor": "rgba(54, 162, 235, 1)",
                            "fill": False,
                            "tension": 0.1
                        }]
                    },
                    "options": {
                        "scales": {
                            "x": {"title": {"display": True, "text": "Date"}},
                            "y": {"title": {"display": True, "text": col}}
                        }
                    }
                }
                charts.append({
                    "id": chart_id,
                    "title": f"Line Plot of {col}",
                    "config": config,
                    "description": f"Line plot of {col} over time.",
                    "error": False
                })
            except Exception:
                charts.append({
                    "id": chart_id,
                    "title": f"Line Plot of {col}",
                    "config": {},
                    "description": f"Could not generate line plot for {col}.",
                    "error": True
                })
    
    # 4. Pie chart for categorical cols with ≤10 categories
    for col in cat_cols:
        if df[col].nunique() <= 10:
            chart_id = str(uuid.uuid4()).replace('-', '')[:8]
            try:
                counts = df[col].value_counts()
                colors = [
                    "#FF6384", "#36A2EB", "#FFCE56", "#AA66CC", "#99CC00",
                    "#FF9F40", "#66FF66", "#FF6666", "#6699FF", "#CCCC00"
                ][:len(counts)]
                config = {
                    "type": "pie",
                    "data": {
                        "labels": counts.index.tolist(),
                        "datasets": [{
                            "data": counts.tolist(),
                            "backgroundColor": colors
                        }]
                    },
                    "options": {
                        "plugins": {"legend": {"display": True}}
                    }
                }
                charts.append({
                    "id": chart_id,
                    "title": f"Pie Chart of {col}",
                    "config": config,
                    "description": f"Pie chart showing distribution of {col}.",
                    "error": False
                })
            except Exception:
                charts.append({
                    "id": chart_id,
                    "title": f"Pie Chart of {col}",
                    "config": {},
                    "description": f"Could not generate pie chart for {col}.",
                    "error": True
                })
    
    
    # Example: Bar chart for categorical features with limited categories
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    for col in cat_cols:
        if df[col].nunique() > 20:
            continue  # skip too many categories
        chart_id = str(uuid.uuid4()).replace('-', '')[:8]
        try:
            counts = df[col].value_counts()
            bar_config = {
                "type": "bar",
                "data": {
                    "labels": counts.index.tolist(),
                    "datasets": [{
                        "label": col,
                        "data": counts.tolist(),
                        "backgroundColor": "#99CC00"
                    }]
                },
                "options": {
                    "responsive": True,
                    "plugins": {"legend": {"display": False}},
                    "scales": {
                        "x": {"title": {"display": True, "text": col}},
                        "y": {"title": {"display": True, "text": "Count"}}
                    }
                }
            }
            charts.append({
                "id": chart_id,
                "title": f"Bar chart of {col}",
                "config": bar_config,
                "description": f"Value counts of categorical column {col}.",
                "error": False
            })
        except Exception:
            charts.append({
                "id": chart_id,
                "title": f"Bar chart of {col}",
                "config": {},
                "description": f"Could not plot bar chart of {col}.",
                "error": True
            })
    
    # line plot 
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    for col in num_cols:
        chart_id = str(uuid.uuid4()).replace('-', '')[:8]
        try:
            line_config = {
            "type": "line",
            "data": {
                "labels": df.index.astype(str).tolist(),
                "datasets": [{
                    "label": col,
                    "data": df[col].tolist(),
                    "fill": False,
                    "borderColor": "rgba(54, 162, 235, 0.7)",
                    "tension": 0.1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {"legend": {"display": True}},
                "scales": {
                    "x": {"title": {"display": True, "text": "Index"}},
                    "y": {"title": {"display": True, "text": col}}
                }
            }
            }
            charts.append({
               "id": chart_id,
             "title": f"Line plot of {col}",
                 "config": line_config,
             "description": f"Line plot of numeric column {col} over index.",
             "error": False
            })
        except Exception:
            charts.append({
            "id": chart_id,
            "title": f"Line plot of {col}",
            "config": {},
            "description": f"Could not plot line plot of {col}.",
            "error": True
            })

    # area plot 
    for col in num_cols:
        chart_id = str(uuid.uuid4()).replace('-', '')[:8]
        try:
            area_config = {
            "type": "line",
            "data": {
                "labels": df.index.astype(str).tolist(),
                "datasets": [{
                    "label": col,
                    "data": df[col].tolist(),
                    "fill": True,
                    "backgroundColor": "rgba(75, 192, 192, 0.4)",
                    "borderColor": "rgba(75, 192, 192, 1)",
                    "tension": 0.1
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {"legend": {"display": True}},
                "scales": {
                    "x": {"title": {"display": True, "text": "Index"}},
                    "y": {"title": {"display": True, "text": col}}
                }
            }
            }
            charts.append({
                "id": chart_id,
                "title": f"Area plot of {col}",
                "config": area_config,
                "description": f"Area plot of numeric column {col} over index.",
                "error": False
            })
        except Exception:
            charts.append({
            "id": chart_id,
            "title": f"Area plot of {col}",
            "config": {},
            "description": f"Could not plot area plot of {col}.",
            "error": True
            })

    
    # bubble plot 
    # num_cols_for_bubble = [col for col in num_cols if df[col].notnull().all()]

    # Try to generate bubble plots from combinations of 3 numeric cols
    # for x_col, y_col, size_col in combinations(num_cols_for_bubble, 3):
    #     chart_id = str(uuid.uuid4()).replace('-', '')[:8]
    #     try:
    #         bubble_config = {
    #          "type": "bubble",
    #          "data": {
    #             "datasets": [{
    #                 "label": f'{x_col} vs {y_col} sized by {size_col}',
    #                 "data": [
    #                     {"x": x, "y": y, "r": max(r / 10, 2)}  # scale radius, minimum 2
    #                     for x, y, r in zip(df[x_col], df[y_col], df[size_col])
    #                 ],
    #                 "backgroundColor": "#C21A3E"
    #             }]
    #             },
    #          "options": {
    #             "responsive": True,
    #             "plugins": {"legend": {"display": True}},
    #             "scales": {
    #                 "x": {"title": {"display": True, "text": x_col}},
    #                 "y": {"title": {"display": True, "text": y_col}}
    #             }
    #         }
    #         }
    #         charts.append({
    #           "id": chart_id,
    #          "title": f"Bubble plot: {x_col} vs {y_col} sized by {size_col}",
    #          "config": bubble_config,
    #             "description": f"Bubble plot using {x_col}, {y_col} and size {size_col}.",
    #          "error": False
    #      })
            
    #     except Exception:
    #         charts.append({
    #         "id": chart_id,
    #         "title": f"Bubble plot: {x_col} vs {y_col} sized by {size_col}",
    #         "config": {},
    #         "description": f"Could not plot bubble plot for {x_col}, {y_col}, {size_col}.",
    #         "error": True
    #     })
    #     break  # generate just one bubble plot for demo



    # kde plot 
    from scipy.stats import gaussian_kde

    for col in num_cols:
        chart_id = str(uuid.uuid4()).replace('-', '')[:8]
        try:
            data = df[col].dropna().values
            kde = gaussian_kde(data)
            x_vals = np.linspace(data.min(), data.max(), 200)
            y_vals = kde(x_vals)
            kde_config = {
            "type": "line",
            "data": {
                "labels": x_vals.round(2).astype(str).tolist(),
                "datasets": [{
                    "label": f'KDE of {col}',
                    "data": y_vals.tolist(),
                    "fill": True,
                    "backgroundColor": "rgba(153, 102, 255, 0.4)",
                    "borderColor": "rgba(153, 102, 255, 1)",
                    "tension": 0.3
                }]
            },
            "options": {
                "responsive": True,
                "plugins": {"legend": {"display": True}},
                "scales": {
                    "x": {"title": {"display": True, "text": col}},
                    "y": {"title": {"display": True, "text": "Density"}}
                }
            }
            }
            charts.append({
             "id": chart_id,
             "title": f"KDE plot of {col}",
             "config": kde_config,
            "description": f"Kernel Density Estimate plot of numeric column {col}.",
                "error": False
            })
        except Exception:
         charts.append({
            "id": chart_id,
            "title": f"KDE plot of {col}",
            "config": {},
            "description": f"Could not plot KDE plot of {col}.",
            "error": True
        })




    return charts
