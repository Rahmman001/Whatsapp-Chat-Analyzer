import streamlit as st 
import preprocessor
import helper 
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd
import datetime
import altair as alt

# ==========================================
# 1. PAGE CONFIGURATION & METADATA
# ==========================================
st.set_page_config(
    page_title="Chatalyze | Professional Analytics", 
    layout="wide", 
    page_icon="💬",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. ENTERPRISE SaaS CSS INJECTION
# ==========================================
st.markdown("""
    <style>
    /* Main App Styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Metric Card Styling */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
    }
    /* Dark mode support for metrics */
    @media (prefers-color-scheme: dark) {
        div[data-testid="stMetric"] {
            background-color: #1e1e1e;
            border: 1px solid #2d2d2d;
        }
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 16px;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        border-bottom: 3px solid #0052cc !important;
        color: #0052cc !important;
    }
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Set global plotting style for professional look
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({'figure.autolayout': True})

# ==========================================
# 3. DATA PROCESSING CACHE
# ==========================================
@st.cache_data(show_spinner=False)
def load_and_process_data(raw_data):
    """Caches the dataframe so interactions (dropdowns/sliders) are instant."""
    return preprocessor.preprocess(raw_data)

# ==========================================
# 4. APP HEADER & ONBOARDING UI
# ==========================================
st.title('💬 Chatalyze: Workspace Analytics')
st.markdown("""
Welcome to the professional communication dashboard. Upload your exported WhatsApp `.txt` file to generate secure, client-side insights into team engagement, activity hot-spots, and lexical trends. 
*All processing is done locally; your data is not stored.*
""")

# File Uploader
uploaded_file = st.file_uploader("Drop your conversation export here (.txt)", type=["txt"])

# ==========================================
# 5. MAIN APPLICATION LOGIC
# ==========================================
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    
    with st.spinner("Crunching telemetry data..."):
        df = load_and_process_data(data)
    
    # Fire a success toast (Real web-app feel)
    st.toast('Dataset successfully loaded and parsed!', icon='✅')
    
    # ------------------------------------------
    # CONTROLS & FILTERS (Main Page)
    # ------------------------------------------
    st.markdown("### 🎛️ Analysis Parameters")
    
    # Fetch unique users
    user_list = df['user'].unique().tolist()
    if "group_notification" in user_list:
        user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0, 'Overall')

    ctrl_col1, ctrl_col2 = st.columns([1, 2])
    
    with ctrl_col1:
        selected_user = st.selectbox(
            'Target User / Group', 
            user_list, 
            help="Select 'Overall' for a macro-level view, or isolate a specific user's footprint."
        )
        
    with ctrl_col2:
        # Complex global date filter
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        selected_dates = st.slider(
            "Filter Timeframe",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            format="MMM DD, YYYY"
        )
    
    # Apply Date Filter globally to the dataframe BEFORE passing to helper
    mask = (df['date'].dt.date >= selected_dates[0]) & (df['date'].dt.date <= selected_dates[1])
    filtered_df = df.loc[mask]

    st.markdown("---")
    
    # ------------------------------------------
    # CORE METRICS (KPIs)
    # ------------------------------------------
    num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, filtered_df)
    
    st.markdown(f"#### 📊 High-Level Overview: {selected_user}")
    
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1:
        st.metric(label="Total Messages Captured", value=f"{num_messages:,}", delta="Volume")
    with kpi2:
        st.metric(label="Lexical Word Count", value=f"{words:,}", delta="Activity")
    with kpi3:
        st.metric(label="Media Assets Shared", value=f"{num_media_messages:,}", delta="Files", delta_color="off")
    with kpi4:
        st.metric(label="External Links Routed", value=f"{links:,}", delta="URLs", delta_color="off")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ------------------------------------------
    # DASHBOARD TABS
    # ------------------------------------------
    tab1, tab2, tab3 = st.tabs([
        "📈 Engagement Timelines & Activity", 
        "🧠 Semantic & Sentiment Analysis", 
        "👥 Network Distribution"
    ])
    
    # TAB 1: ACTIVITY
    with tab1:
        st.markdown("""
        ### Temporal Distribution
        *This module analyzes the historical distribution of communications to identify behavioral trends and peak engagement periods over the selected timeframe.*
        """)
        
        t_col1, t_col2 = st.columns(2)
        
        with t_col1:
            st.markdown("**Monthly Macro Trend**")
            timeline = helper.monthly_timeline(selected_user, filtered_df)
            if not timeline.empty:
                st.area_chart(timeline.set_index('time')['message'], color="#4a90e2")
            else:
                st.info("Not enough data in this timeframe.")
                
        with t_col2:
            st.markdown("**Daily Micro Trend**")
            daily_timeline = helper.daily_timeline(selected_user, filtered_df)
            if not daily_timeline.empty:
                st.line_chart(daily_timeline.set_index('only_date')['message'], color="#e24a7b")
            else:
                st.info("Not enough data in this timeframe.")
            
        st.markdown("---")
        
        st.markdown("### Operational Heatmaps")
        st.caption("Identify when your network is most active. Darker zones indicate high-traffic communication windows.")
        
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            busy_day = helper.week_activity_map(selected_user, filtered_df)
            st.markdown("**Traffic by Day of Week**")
            st.bar_chart(busy_day, color="#8884d8")
            
        with a_col2:
            busy_month = helper.month_activity_map(selected_user, filtered_df)
            st.markdown("**Traffic by Month of Year**")
            st.bar_chart(busy_month, color="#82ca9d")

        st.markdown("**Hourly Heatmap (Density View)**")
        user_heatmap = helper.activity_heatmap(selected_user, filtered_df)
        
        fig, ax = plt.subplots(figsize=(12, 4))
        
        # Make the figure background transparent so it blends perfectly with the app
        fig.patch.set_facecolor('none') 
        ax.set_facecolor('none')
        
        # Use a high-contrast, glowing colormap (magma, plasma, or inferno)
        sns.heatmap(
            user_heatmap, 
            cmap="magma", 
            ax=ax, 
            linewidths=0.5, 
            linecolor='#333333', 
            cbar_kws={'label': 'Msg Volume'}
        )
        
        # Force all text and ticks to be white so they pop
        ax.tick_params(colors='white', which='both')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        
        # Fix the colorbar text color
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
        cbar.set_label('Msg Volume', color='white')

        plt.xlabel("Time of Day")
        plt.ylabel("Day of Week")
        st.pyplot(fig)
        
    # TAB 2: SEMANTICS
    with tab2:
        st.markdown("""
        ### Lexical Footprint
        *Understanding the vocabulary and non-verbal cues (emojis) provides insight into the tonal footprint and primary subjects of the conversation.*
        """)
        
        w_col1, w_col2 = st.columns(2)
        
        with w_col1:
            st.markdown("**Semantic Word Cloud**")
            with st.container(border=True):
                try:
                    df_wc = helper.create_wordcloud(selected_user, filtered_df)
                    fig, ax = plt.subplots(figsize=(6, 6))
                    ax.imshow(df_wc, interpolation='bilinear')
                    ax.axis("off")
                    st.pyplot(fig)
                except ValueError:
                    st.warning("Insufficient text data to generate a word cloud.")
            
        with w_col2:
            st.markdown("**Highest Frequency Terms**")
            most_common_df = helper.most_common_words(selected_user, filtered_df)
            if not most_common_df.empty:
                st.bar_chart(most_common_df.set_index(0)[1], color="#4a90e2")
            else:
                st.info("Insufficient valid words to display common words visualization.")
                
        st.markdown("---")
        
        st.markdown("### Emoji Utilization Analysis")
        e_col1, e_col2 = st.columns([1, 2])
        emoji_df = helper.emoji_helper(selected_user, filtered_df)
        
        if not emoji_df.empty:
            with e_col1:
                st.dataframe(
                    emoji_df.rename(columns={'emoji': 'Symbol', 'count': 'Frequency'}), 
                    width="stretch",
                    hide_index=True
                )
            with e_col2:
                top_emojis = emoji_df.head(8)
                
                # Build an interactive donut chart with EXPLICIT sizing
                donut = alt.Chart(top_emojis).mark_arc(innerRadius=90, outerRadius=140).encode(
                    theta=alt.Theta(field="count", type="quantitative"),
                    color=alt.Color(
                        field="emoji", 
                        type="nominal", 
                        legend=None, 
                        scale=alt.Scale(scheme='pastel1')
                    ),
                    tooltip=[
                        alt.Tooltip("emoji", title="Emoji"), 
                        alt.Tooltip("count", title="Frequency")
                    ]
                )
                
                # Add the emojis as text floating just outside the donut slices
                text = alt.Chart(top_emojis).mark_text(radius=175, size=28).encode(
                    theta=alt.Theta(field="count", type="quantitative", stack=True),
                    text=alt.Text(field="emoji", type="nominal")
                )
                
                # Combine the charts and force a minimum height so it doesn't collapse
                final_chart = (donut + text).configure_view(
                    strokeWidth=0
                ).properties(
                    height=450,
                    background='transparent'
                )
                
                st.altair_chart(final_chart, use_container_width=True)
        else:
            st.info("No emojis detected in the filtered dataset.")
            
    # TAB 3: NETWORK
    with tab3:
        if selected_user == 'Overall':
            st.markdown("""
            ### Group Dynamics & Contribution
            *Observe how different entities contribute to the overall communication ecosystem. Who are the primary drivers of conversation?*
            """)
            
            x, new_df = helper.most_busy_users(filtered_df)
            
            u_col1, u_col2 = st.columns(2)
            with u_col1:
                st.markdown("**Top Contributors (Absolute Volume)**")
                st.bar_chart(x, color="#ff7f50")
                
            with u_col2:
                st.markdown("**Share of Voice (Percentage)**")
                
                # Force correct column names regardless of Pandas version
                new_df.columns = ['User Identifier', 'Contribution (%)']
                
                # Safely apply the gradient
                st.dataframe(
                    new_df.style.background_gradient(cmap='Blues', subset=['Contribution (%)']), 
                    width="stretch",
                    hide_index=True
                )
        else:
            st.warning("⚠️ Network Distribution is only available in the 'Overall' macro view. Please change the Target User in the Analysis Parameters above.")

else:
    # ------------------------------------------
    # EMPTY STATE (When no file is uploaded)
    # ------------------------------------------
    st.info("👆 Please use the file uploader above to initialize the dashboard.")
    
    with st.expander("📖 How to export your WhatsApp Data"):
        st.markdown("""
        1. Open the WhatsApp chat you want to analyze.
        2. Tap the **Three Dots (Menu)** in the top right corner.
        3. Tap **More** > **Export Chat**.
        4. Choose **Without Media** (this app analyzes text data).
        5. Save the generated `.txt` file to your device.
        6. Upload that file right here!
        """)