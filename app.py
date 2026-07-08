import streamlit as st
import streamlit.components.v1 as components
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import altair as alt

# ==========================================
# 1. PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Chatalyze | Professional Analytics",
    layout="wide",
    page_icon="💬",
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. AURORA DARK — LOAD CSS FROM FILE
# ==========================================
# CSS is in style.css (not inlined) because Streamlit's markdown parser
# treats `*` as a bullet point, rendering inline CSS as visible text.
with open("style.css") as _f:
    st.markdown(f"<style>{_f.read()}</style>", unsafe_allow_html=True)

# Google Fonts
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

# ==========================================
# 3. DARK PLOTTING THEME
# ==========================================
plt.style.use('dark_background')
sns.set_theme(style="darkgrid", palette="pastel")
plt.rcParams.update({
    'figure.autolayout': True,
    'figure.facecolor': 'none',
    'axes.facecolor': '#0d0d1a',
    'axes.edgecolor': (1, 1, 1, 0.08),
    'axes.labelcolor': '#86868b',
    'xtick.color': '#86868b',
    'ytick.color': '#86868b',
    'grid.color': (1, 1, 1, 0.05),
    'grid.linewidth': 0.8,
    'text.color': '#f5f5f7',
    'font.family': 'sans-serif',
})

# ==========================================
# 4. CACHE
# ==========================================
@st.cache_data
def load_and_process_data(raw_data):
    return preprocessor.preprocess(raw_data)

# ==========================================
# 5. AURORA BACKGROUND DIVS
# ==========================================
st.markdown('<div id="aurora"></div><div id="aurora-glow"></div>', unsafe_allow_html=True)

# ==========================================
# 6. HERO HEADER
# ==========================================
st.markdown("""
<div style="padding:4rem 0 3rem; animation:fade-up 0.8s cubic-bezier(0.16,1,0.3,1) both;">

  <div style="display:inline-flex;align-items:center;gap:7px;
    background:rgba(120,80,255,0.12);border:1px solid rgba(120,80,255,0.3);
    border-radius:100px;padding:5px 14px 5px 10px;margin-bottom:1.8rem;">
    <span style="width:7px;height:7px;background:#7850ff;border-radius:50%;
      display:inline-block;box-shadow:0 0 8px #7850ff;
      animation:aurora-pulse 2s ease-in-out infinite alternate;"></span>
    <span style="font-size:0.72rem;font-weight:600;color:rgba(180,150,255,0.9);
      letter-spacing:0.1em;text-transform:uppercase;">Local · Private · Instant</span>
  </div>

  <h1 style="
    font-size:clamp(3.5rem,8vw,7rem); font-weight:900; line-height:0.95;
    letter-spacing:-0.045em; margin:0 0 1.5rem;
    background:linear-gradient(160deg,#ffffff 0%,#c4b5fd 30%,#818cf8 55%,#38bdf8 80%,#ffffff 100%);
    background-size:300% auto; -webkit-background-clip:text;
    -webkit-text-fill-color:transparent; background-clip:text;
    animation:shimmer 6s linear infinite;">Chatalyze</h1>

  <p style="font-size:clamp(1rem,2vw,1.2rem);color:rgba(255,255,255,0.45);
    font-weight:400;max-width:500px;line-height:1.7;margin:0;letter-spacing:-0.01em;">
    Turn your WhatsApp exports into stunning analytics.<br>
    Everything runs in your browser. Zero data leaves your device.
  </p>

</div>
""", unsafe_allow_html=True)

# ==========================================
# 7. FILE UPLOADER
# ==========================================
uploaded_file = st.file_uploader("Drop your conversation export here (.txt)", type=["txt"])

# JS: fix Streamlit's upload button double-text (SVG icon bleeds over label)
components.html("""
<script>
function fixBtn() {
    try {
        const doc = window.parent.document;
        const btn = doc.querySelector('[data-testid="stFileUploaderDropzone"] button');
        if (!btn) return;
        btn.querySelectorAll('svg').forEach(el => el.style.display = 'none');
        const spans = btn.querySelectorAll('span');
        if (spans.length > 1) {
            for (let i = 0; i < spans.length - 1; i++) spans[i].style.display = 'none';
        }
    } catch(e) {}
}
fixBtn(); setTimeout(fixBtn,300); setTimeout(fixBtn,800); setTimeout(fixBtn,2000);
new MutationObserver(fixBtn).observe(window.parent.document.body,{childList:true,subtree:true});
</script>
""", height=0)

# ==========================================
# 8. MAIN APP LOGIC
# ==========================================
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    with st.spinner("Crunching telemetry data..."):
        df = load_and_process_data(data)

    st.toast('Dataset successfully loaded and parsed!', icon='✅')

    # CONTROLS
    st.markdown("### 🎛️ Analysis Parameters")

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
            help="Select 'Overall' for a macro-level view, or isolate a specific user."
        )
    with ctrl_col2:
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        selected_dates = st.slider(
            "Filter Timeframe",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            format="MMM DD, YYYY"
        )

    mask = (df['date'].dt.date >= selected_dates[0]) & (df['date'].dt.date <= selected_dates[1])
    filtered_df = df.loc[mask]
    st.markdown("---")

    # KPIs
    num_messages, words, num_media_messages, links = helper.fetch_stats(selected_user, filtered_df)
    st.markdown(f"#### 📊 High-Level Overview: {selected_user}")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    with kpi1: st.metric(label="Total Messages", value=f"{num_messages:,}", delta="Volume")
    with kpi2: st.metric(label="Word Count", value=f"{words:,}", delta="Activity")
    with kpi3: st.metric(label="Media Shared", value=f"{num_media_messages:,}", delta="Files", delta_color="off")
    with kpi4: st.metric(label="Links Shared", value=f"{links:,}", delta="URLs", delta_color="off")

    st.markdown("<br>", unsafe_allow_html=True)

    # TABS
    tab1, tab2, tab3 = st.tabs([
        "📈 Engagement Timelines & Activity",
        "🧠 Semantic & Sentiment Analysis",
        "👥 Network Distribution"
    ])

    with tab1:
        st.markdown("""
        ### Temporal Distribution
        *Historical distribution of communications to identify behavioral trends and peak engagement periods.*
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
        st.caption("Identify when your network is most active. Darker zones indicate high-traffic windows.")
        a_col1, a_col2 = st.columns(2)
        with a_col1:
            busy_day = helper.week_activity_map(selected_user, filtered_df)
            st.markdown("**Traffic by Day of Week**")
            st.bar_chart(busy_day, color="#8884d8")
        with a_col2:
            busy_month = helper.month_activity_map(selected_user, filtered_df)
            st.markdown("**Traffic by Month**")
            st.bar_chart(busy_month, color="#82ca9d")

        st.markdown("**Hourly Heatmap (Density View)**")
        user_heatmap = helper.activity_heatmap(selected_user, filtered_df)
        fig, ax = plt.subplots(figsize=(12, 4))
        fig.patch.set_facecolor('none')
        ax.set_facecolor('none')
        sns.heatmap(user_heatmap, cmap="magma", ax=ax, linewidths=0.5,
                    linecolor='#222', cbar_kws={'label': 'Msg Volume'})
        ax.tick_params(colors='white', which='both')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        cbar = ax.collections[0].colorbar
        cbar.ax.yaxis.set_tick_params(color='white', labelcolor='white')
        cbar.set_label('Msg Volume', color='white')
        plt.xlabel("Time of Day")
        plt.ylabel("Day of Week")
        st.pyplot(fig)

    with tab2:
        st.markdown("""
        ### Lexical Footprint
        *Understanding vocabulary and emoji usage provides insight into the tonal footprint of the conversation.*
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
                st.info("Insufficient valid words to display.")

        st.markdown("---")
        st.markdown("### Emoji Utilization Analysis")
        e_col1, e_col2 = st.columns([1, 2])
        emoji_df = helper.emoji_helper(selected_user, filtered_df)
        if not emoji_df.empty:
            with e_col1:
                st.dataframe(
                    emoji_df.rename(columns={'emoji': 'Symbol', 'count': 'Frequency'}),
                    width="stretch", hide_index=True
                )
            with e_col2:
                top_emojis = emoji_df.head(8)
                donut = alt.Chart(top_emojis).mark_arc(innerRadius=90, outerRadius=140).encode(
                    theta=alt.Theta(field="count", type="quantitative"),
                    color=alt.Color(field="emoji", type="nominal", legend=None,
                                    scale=alt.Scale(scheme='pastel1')),
                    tooltip=[alt.Tooltip("emoji", title="Emoji"), alt.Tooltip("count", title="Frequency")]
                )
                text = alt.Chart(top_emojis).mark_text(radius=175, size=28).encode(
                    theta=alt.Theta(field="count", type="quantitative", stack=True),
                    text=alt.Text(field="emoji", type="nominal")
                )
                final_chart = (donut + text).configure_view(strokeWidth=0).properties(
                    height=450, background='transparent'
                )
                st.altair_chart(final_chart, use_container_width=True)
        else:
            st.info("No emojis detected in the filtered dataset.")

    with tab3:
        if selected_user == 'Overall':
            st.markdown("""
            ### Group Dynamics & Contribution
            *Who are the primary drivers of conversation?*
            """)
            x, new_df = helper.most_busy_users(filtered_df)
            u_col1, u_col2 = st.columns(2)
            with u_col1:
                st.markdown("**Top Contributors (Volume)**")
                st.bar_chart(x, color="#ff7f50")
            with u_col2:
                st.markdown("**Share of Voice (%)**")
                new_df.columns = ['User Identifier', 'Contribution (%)']
                st.dataframe(
                    new_df.style.background_gradient(cmap='Blues', subset=['Contribution (%)']),
                    width="stretch", hide_index=True
                )
        else:
            st.warning("⚠️ Network Distribution is only available in the 'Overall' view.")

else:
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