import plotly.graph_objects as go
fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 5, 20])])
# Save to an HTML file
fig.write_html('plot.html')
