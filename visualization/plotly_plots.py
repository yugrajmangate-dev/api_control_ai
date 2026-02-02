import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np


def plot_seir_plotly(metrics):
    days = list(range(len(metrics["overall"]["S"])))

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        subplot_titles=[
            "Overall SEIR",
            "Children SEIR",
            "Adults SEIR"
        ]
    )

    def add_traces(group, row):
        fig.add_trace(go.Scatter(x=days, y=metrics[group]["S"], name="S"), row=row, col=1)
        fig.add_trace(go.Scatter(x=days, y=metrics[group]["E"], name="E"), row=row, col=1)
        fig.add_trace(go.Scatter(x=days, y=metrics[group]["I"], name="I"), row=row, col=1)
        fig.add_trace(go.Scatter(x=days, y=metrics[group]["R"], name="R"), row=row, col=1)

    add_traces("overall", 1)
    add_traces("children", 2)
    add_traces("adults", 3)

    fig.update_layout(
        height=800,
        title_text="SEIR Dynamics (Overall + Age-wise)",
        showlegend=True
    )

    fig.update_xaxes(title_text="Days")
    fig.update_yaxes(title_text="Population Count")

    return fig


def plot_infection_heatmap(population, grid_size=20, title="Infection Hotspot Heatmap"):
    """
    Create 2D heatmap showing spatial distribution of infections
    
    Args:
        population: List of agents with x, y coordinates
        grid_size: Number of grid cells (grid_size x grid_size)
        title: Plot title
    
    Returns:
        Plotly figure object
    """
    # Initialize grid
    infection_grid = np.zeros((grid_size, grid_size))
    total_grid = np.zeros((grid_size, grid_size))
    
    # Count infected and total agents in each cell
    for agent in population:
        if "x" not in agent or "y" not in agent:
            continue
        
        # Map coordinates to grid cells
        x_bin = min(int(agent["x"] * grid_size), grid_size - 1)
        y_bin = min(int(agent["y"] * grid_size), grid_size - 1)
        
        total_grid[y_bin, x_bin] += 1
        
        if agent["state"] in ["I", "E"]:  # Infected or Exposed
            infection_grid[y_bin, x_bin] += 1
    
    # Calculate infection rate per cell (avoid division by zero)
    infection_rate_grid = np.divide(
        infection_grid, 
        total_grid, 
        out=np.zeros_like(infection_grid),
        where=total_grid != 0
    )
    
    # Create heatmap with better styling
    fig = px.imshow(
        infection_rate_grid,
        labels=dict(x="Geographic Region (X)", y="Geographic Region (Y)", color="Infection Rate"),
        color_continuous_scale=[
            [0, '#ffffff'],      # White for no infection
            [0.2, '#fee2e2'],    # Very light red
            [0.4, '#fca5a5'],    # Light red
            [0.6, '#f87171'],    # Medium red
            [0.8, '#dc2626'],    # Red
            [1.0, '#7f1d1d']     # Dark red
        ],
        title=title,
        aspect="auto"
    )
    
    fig.update_layout(
        width=600,
        height=500,
        xaxis=dict(
            title="Geographic Region (X)",
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title="Geographic Region (Y)",
            showgrid=False,
            zeroline=False
        ),
        coloraxis_colorbar=dict(
            title="Infection<br>Rate",
            tickformat=".0%",
            len=0.7
        )
    )
    
    # Add text annotations for high infection cells
    max_rate = infection_rate_grid.max()
    if max_rate > 0:
        for i in range(grid_size):
            for j in range(grid_size):
                if infection_rate_grid[i, j] > 0.7 * max_rate and infection_rate_grid[i, j] > 0:
                    fig.add_annotation(
                        x=j, y=i,
                        text=f"{infection_rate_grid[i, j]:.0%}",
                        showarrow=False,
                        font=dict(size=9, color='white', family='Arial Black')
                    )
    
    return fig


def plot_spatial_scatter(population, title="Population Distribution by State"):
    """
    Create scatter plot showing agent positions colored by SEIR state
    
    Args:
        population: List of agents with x, y coordinates
        title: Plot title
    
    Returns:
        Plotly figure object
    """
    # Extract data
    x_coords = []
    y_coords = []
    states = []
    
    # Define colors and labels for SEIR states
    state_info = {
        "S": {"color": "#3b82f6", "label": "Susceptible"},
        "E": {"color": "#f59e0b", "label": "Exposed"},
        "I": {"color": "#ef4444", "label": "Infected"},
        "R": {"color": "#10b981", "label": "Recovered"}
    }
    
    for agent in population:
        if "x" not in agent or "y" not in agent:
            continue
        
        x_coords.append(agent["x"])
        y_coords.append(agent["y"])
        states.append(agent["state"])
    
    # Create scatter plot
    fig = go.Figure()
    
    # Add traces in specific order: S, E, I, R
    for state in ["S", "E", "I", "R"]:
        mask = [s == state for s in states]
        x_filtered = [x for x, m in zip(x_coords, mask) if m]
        y_filtered = [y for y, m in zip(y_coords, mask) if m]
        
        if not x_filtered:  # Skip if no agents in this state
            continue
        
        fig.add_trace(go.Scatter(
            x=x_filtered,
            y=y_filtered,
            mode='markers',
            name=f'{state_info[state]["label"]} ({len(x_filtered)})',
            marker=dict(
                size=6,
                color=state_info[state]["color"],
                opacity=0.7,
                line=dict(width=0.5, color='white')
            ),
            hovertemplate=f'<b>{state_info[state]["label"]}</b><br>X: %{{x:.2f}}<br>Y: %{{y:.2f}}<extra></extra>'
        ))
    
    fig.update_layout(
        title=title,
        xaxis=dict(
            title="X Position",
            range=[0, 1],
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        yaxis=dict(
            title="Y Position",
            range=[0, 1],
            showgrid=True,
            gridcolor='rgba(128,128,128,0.2)'
        ),
        width=600,
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor="rgba(255,255,255,0.8)",
            bordercolor="gray",
            borderwidth=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        hovermode='closest'
    )
    
    return fig


def plot_mutation_timeline(mutation_tracker, metrics):
    """
    Create timeline showing when mutations occurred and their impact
    
    Args:
        mutation_tracker: MutationTracker object
        metrics: Simulation metrics dictionary
    
    Returns:
        Plotly figure object
    """
    mutations = mutation_tracker.get_summary()["events"]
    
    if not mutations:
        # Return empty figure if no mutations
        fig = go.Figure()
        fig.add_annotation(
            text="No mutations occurred during simulation",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=14)
        )
        return fig
    
    days = list(range(len(metrics["overall"]["I"])))
    infected = metrics["overall"]["I"]
    
    fig = go.Figure()
    
    # Plot infection curve
    fig.add_trace(go.Scatter(
        x=days,
        y=infected,
        mode='lines',
        name='Infected Count',
        line=dict(color='#ef4444', width=3),
        fill='tonexty',
        fillcolor='rgba(239, 68, 68, 0.1)'
    ))
    
    # Group mutations that occur on the same day to avoid overlapping annotations
    mutation_days = {}
    for mut in mutations:
        day = mut["day"]
        if day not in mutation_days:
            mutation_days[day] = []
        mutation_days[day].append(mut)
    
    # Add mutation markers - one per unique day with combined information
    for day, day_mutations in mutation_days.items():
        if day >= len(infected):
            continue
            
        # Add vertical line at mutation day
        fig.add_vline(
            x=day,
            line=dict(dash="dash", color="rgba(168, 85, 247, 0.6)", width=2),
            annotation=dict(
                text=f"Day {day}: {len(day_mutations)} mutation(s)",
                textangle=-90,
                font=dict(size=10, color="purple")
            )
        )
        
        # Add scatter point for mutation event
        mutation_info = []
        for mut in day_mutations:
            r0_change = mut["changes"]["R0"]["change_pct"]
            mutation_info.append(f"Strain {mut['strain_number']}: R₀ +{r0_change:.1f}%")
        
        fig.add_trace(go.Scatter(
            x=[day],
            y=[infected[day]],
            mode='markers',
            name=f'Mutation Day {day}',
            marker=dict(
                size=12,
                color='purple',
                symbol='diamond',
                line=dict(color='white', width=2)
            ),
            hovertext="<br>".join(mutation_info),
            hoverinfo='text',
            showlegend=False
        ))
    
    fig.update_layout(
        title="Mutation Events Timeline",
        xaxis_title="Day",
        yaxis_title="Infected Count",
        showlegend=True,
        height=450,
        hovermode='closest',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(128,128,128,0.2)')
    
    return fig


def plot_policy_comparison(comparison_results):
    """
    Create comparison charts for different policy strategies
    
    Args:
        comparison_results: Dictionary with policy names as keys, metrics as values
    
    Returns:
        Plotly figure object
    """
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=[
            "Peak Infections",
            "Total Deaths",
            "Economic Cost",
            "Final Recovered"
        ],
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    policies = list(comparison_results.keys())
    
    # Extract metrics
    peak_infections = [comparison_results[p]["peak_infected"] for p in policies]
    total_deaths = [comparison_results[p]["total_deaths"] for p in policies]
    economic_costs = [comparison_results[p]["economic_cost"] for p in policies]
    final_recovered = [comparison_results[p]["final_recovered"] for p in policies]
    
    # Add bar charts
    fig.add_trace(go.Bar(x=policies, y=peak_infections, name="Peak Infections", marker_color="red"), row=1, col=1)
    fig.add_trace(go.Bar(x=policies, y=total_deaths, name="Deaths", marker_color="black"), row=1, col=2)
    fig.add_trace(go.Bar(x=policies, y=economic_costs, name="Cost", marker_color="orange"), row=2, col=1)
    fig.add_trace(go.Bar(x=policies, y=final_recovered, name="Recovered", marker_color="green"), row=2, col=2)
    
    fig.update_layout(
        height=600,
        title_text="Policy Comparison Dashboard",
        showlegend=False
    )
    
    return fig


def plot_global_epidemic_map(simulation_metrics=None):
    """
    Create interactive choropleth world map showing global epidemic spread
    
    Args:
        simulation_metrics: Optional metrics from current simulation
    
    Returns:
        Plotly figure object with world map
    """
    import pandas as pd
    
    # Simulated global epidemic data (based on realistic patterns)
    # In a real scenario, this would come from WHO/CDC global surveillance data
    global_data = pd.DataFrame({
        'country': [
            'USA', 'India', 'China', 'Brazil', 'United Kingdom', 'Germany', 'France', 
            'Italy', 'Spain', 'Canada', 'Japan', 'South Korea', 'Australia', 'Mexico',
            'Indonesia', 'Turkey', 'Saudi Arabia', 'Iran', 'Egypt', 'South Africa',
            'Nigeria', 'Kenya', 'Argentina', 'Colombia', 'Chile', 'Peru', 'Russia',
            'Poland', 'Ukraine', 'Thailand', 'Vietnam', 'Philippines', 'Pakistan',
            'Bangladesh', 'Malaysia', 'Singapore', 'New Zealand', 'Israel', 'UAE',
            'Sweden', 'Norway', 'Denmark', 'Finland', 'Netherlands', 'Belgium',
            'Switzerland', 'Austria', 'Greece', 'Portugal', 'Czech Republic'
        ],
        'iso_alpha': [
            'USA', 'IND', 'CHN', 'BRA', 'GBR', 'DEU', 'FRA', 'ITA', 'ESP', 'CAN',
            'JPN', 'KOR', 'AUS', 'MEX', 'IDN', 'TUR', 'SAU', 'IRN', 'EGY', 'ZAF',
            'NGA', 'KEN', 'ARG', 'COL', 'CHL', 'PER', 'RUS', 'POL', 'UKR', 'THA',
            'VNM', 'PHL', 'PAK', 'BGD', 'MYS', 'SGP', 'NZL', 'ISR', 'ARE', 'SWE',
            'NOR', 'DNK', 'FIN', 'NLD', 'BEL', 'CHE', 'AUT', 'GRC', 'PRT', 'CZE'
        ],
        'infection_rate': [
            15.2, 12.8, 8.5, 18.3, 14.5, 11.2, 13.8, 16.1, 15.7, 10.3,
            7.2, 6.8, 5.1, 19.4, 14.7, 13.2, 9.8, 11.5, 10.7, 17.8,
            8.9, 12.4, 16.8, 15.3, 14.9, 20.1, 13.6, 12.7, 14.2, 9.3,
            6.5, 13.9, 11.8, 10.4, 8.7, 4.2, 3.8, 10.9, 7.6, 9.1,
            7.8, 8.2, 6.9, 11.4, 12.3, 9.5, 10.2, 13.4, 12.1, 11.9
        ],
        'total_cases': [
            45200000, 44100000, 38500000, 35800000, 24300000, 21500000, 22800000,
            21200000, 20100000, 18700000, 16200000, 15100000, 12400000, 28900000,
            24600000, 19800000, 14200000, 17300000, 15800000, 22100000,
            12800000, 14200000, 20400000, 18900000, 17200000, 25600000, 21800000,
            18400000, 19300000, 13200000, 11500000, 19600000, 16700000, 14900000,
            13400000, 8700000, 6200000, 15300000, 12100000, 13800000,
            11900000, 12600000, 10800000, 17400000, 18200000, 14100000, 15200000,
            19700000, 17900000, 16800000
        ],
        'severity': [
            'High', 'High', 'Medium', 'Very High', 'High', 'Medium', 'High',
            'High', 'High', 'Medium', 'Low', 'Low', 'Low', 'Very High',
            'High', 'High', 'Medium', 'Medium', 'Medium', 'High',
            'Medium', 'Medium', 'High', 'High', 'High', 'Very High', 'High',
            'Medium', 'High', 'Medium', 'Low', 'High', 'Medium', 'Medium',
            'Medium', 'Low', 'Very Low', 'Medium', 'Low', 'Medium',
            'Low', 'Low', 'Low', 'Medium', 'Medium', 'Medium', 'Medium',
            'High', 'Medium', 'Medium'
        ]
    })
    
    # Create choropleth map
    fig = px.choropleth(
        global_data,
        locations="iso_alpha",
        locationmode="ISO-3",
        color="infection_rate",
        hover_name="country",
        hover_data={
            'iso_alpha': False,
            'infection_rate': ':.1f',
            'total_cases': ':,',
            'severity': True
        },
        color_continuous_scale=[
            [0, '#d1fae5'],      # Very light green
            [0.2, '#6ee7b7'],    # Light green
            [0.4, '#fef08a'],    # Yellow
            [0.6, '#fbbf24'],    # Orange
            [0.8, '#f87171'],    # Light red
            [1.0, '#dc2626']     # Dark red
        ],
        projection="natural earth",
        labels={'infection_rate': 'Infection Rate (%)'},
        title="Global Epidemic Spread - Real-time Surveillance Dashboard"
    )
    
    fig.update_layout(
        height=600,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            coastlinecolor='#4b5563',
            projection_type='natural earth',
            bgcolor='rgba(0,0,0,0)',
            landcolor='#1f2937',  # Dark gray for countries with no data
            showland=True
        ),
        coloraxis_colorbar=dict(
            title="Infection<br>Rate (%)",
            thickness=15,
            len=0.7,
            x=0.95
        ),
        font=dict(size=12),
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    # Add annotation with data source
    fig.add_annotation(
        text="Simulated data based on WHO/CDC surveillance patterns | For demonstration purposes",
        xref="paper", yref="paper",
        x=0.5, y=-0.05,
        showarrow=False,
        font=dict(size=10, color="gray")
    )
    
    return fig


def plot_globe_view_3d(simulation_metrics=None):
    """
    Create 3D orthographic (globe) view of epidemic spread
    
    Args:
        simulation_metrics: Optional metrics from current simulation
    
    Returns:
        Plotly figure object with globe view
    """
    import pandas as pd
    
    # Same data as above
    global_data = pd.DataFrame({
        'country': [
            'USA', 'India', 'China', 'Brazil', 'United Kingdom', 'Germany', 'France', 
            'Italy', 'Spain', 'Canada', 'Japan', 'South Korea', 'Australia', 'Mexico',
            'Indonesia', 'Turkey', 'Saudi Arabia', 'Iran', 'Egypt', 'South Africa',
            'Nigeria', 'Kenya', 'Argentina', 'Colombia', 'Chile', 'Russia'
        ],
        'iso_alpha': [
            'USA', 'IND', 'CHN', 'BRA', 'GBR', 'DEU', 'FRA', 'ITA', 'ESP', 'CAN',
            'JPN', 'KOR', 'AUS', 'MEX', 'IDN', 'TUR', 'SAU', 'IRN', 'EGY', 'ZAF',
            'NGA', 'KEN', 'ARG', 'COL', 'CHL', 'RUS'
        ],
        'infection_rate': [
            15.2, 12.8, 8.5, 18.3, 14.5, 11.2, 13.8, 16.1, 15.7, 10.3,
            7.2, 6.8, 5.1, 19.4, 14.7, 13.2, 9.8, 11.5, 10.7, 17.8,
            8.9, 12.4, 16.8, 15.3, 14.9, 13.6
        ]
    })
    
    # Create 3D globe
    fig = px.choropleth(
        global_data,
        locations="iso_alpha",
        locationmode="ISO-3",
        color="infection_rate",
        hover_name="country",
        color_continuous_scale="Reds",
        projection="orthographic",
        title="3D Globe View - Epidemic Hotspots"
    )
    
    fig.update_layout(
        height=550,
        geo=dict(
            showland=True,
            landcolor='#374151',  # Dark gray for countries with no data
            coastlinecolor='#6b7280',
            projection_type='orthographic',
            showocean=True,
            oceancolor='rgb(230, 245, 255)'
        ),
        coloraxis_colorbar=dict(
            title="Rate (%)",
            thickness=15,
            len=0.6
        )
    )
    
    return fig

