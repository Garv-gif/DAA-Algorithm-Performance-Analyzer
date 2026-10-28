
import time
import random
import pandas as pd
import streamlit as st
import plotly.express as px


# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="Algorithm Performance Analyzer",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0b1220, #111c32);
        color: #f1f5f9;
    }

    h1, h2, h3, p, label {
        color: #f1f5f9;
    }

    div[data-testid="stMetric"] {
        background: #18263d;
        border: 1px solid #2b3d59;
        padding: 18px;
        border-radius: 14px;
    }

    div[data-testid="stMetricValue"] {
        color: #60a5fa;
    }

    section[data-testid="stSidebar"] {
        background: #101a2c;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# ==================== SORTING ALGORITHMS ====================

def bubble_sort(arr):
    arr = arr.copy()
    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:
            break

    return arr


def merge_sort(arr):
    if len(arr) <= 1:
        return arr.copy()

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def quick_sort(arr):
    arr = arr.copy()

    def sort(low, high):
        if low >= high:
            return

        pivot_index = random.randint(low, high)
        arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
        pivot = arr[high]

        i = low - 1

        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        i += 1
        arr[i], arr[high] = arr[high], arr[i]

        sort(low, i - 1)
        sort(i + 1, high)

    sort(0, len(arr) - 1)
    return arr


# ==================== SEARCHING ALGORITHMS ====================

def linear_search(arr, target):
    for i, value in enumerate(arr):
        if value == target:
            return i

    return -1


def binary_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


# ==================== ALGORITHM VISUALIZER ====================

def create_bubble_steps(values):
    arr = values.copy()

    steps = [{
        "array": arr.copy(),
        "left": -1,
        "right": -1,
        "message": "Starting array"
    }]

    n = len(arr)

    for i in range(n):
        swapped = False

        for j in range(n - i - 1):
            steps.append({
                "array": arr.copy(),
                "left": j,
                "right": j + 1,
                "message": (
                    f"Comparing {arr[j]} and {arr[j + 1]}"
                )
            })

            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

                steps.append({
                    "array": arr.copy(),
                    "left": j,
                    "right": j + 1,
                    "message": (
                        f"Swapped elements: {arr[j]} and {arr[j + 1]}"
                    )
                })

        if not swapped:
            break

    steps.append({
        "array": arr.copy(),
        "left": -1,
        "right": -1,
        "message": "Sorting completed!"
    })

    return steps


# ==================== PERFORMANCE MEASUREMENT ====================

def time_sort(function, data):
    start = time.perf_counter()
    output = function(data)
    elapsed = (time.perf_counter() - start) * 1000

    if output != sorted(data):
        raise ValueError("Sorting validation failed.")

    return elapsed


def time_search(function, data, target, trials=10):
    start = time.perf_counter()

    for _ in range(trials):
        result = function(data, target)

        if result == -1:
            raise ValueError("Search validation failed.")

    elapsed = (time.perf_counter() - start) * 1000

    return elapsed / trials


# ==================== SESSION STATE ====================

if "results" not in st.session_state:
    st.session_state.results = []

if "visual_steps" not in st.session_state:
    st.session_state.visual_steps = []

if "visual_values" not in st.session_state:
    st.session_state.visual_values = []

if "visual_generation" not in st.session_state:
    st.session_state.visual_generation = 0


# ==================== SIDEBAR ====================

st.sidebar.title("📊 DAA ANALYZER")
st.sidebar.caption("Algorithm Research Dashboard")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Sorting Analysis",
        "Algorithm Visualizer",
        "Searching Analysis",
        "Complexity Guide",
        "Results & Export"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Study algorithm performance through practical testing, "
    "interactive graphs and Big-O complexity."
)


# ==================== HEADER ====================

st.title("Algorithm Performance Analyzer")
st.caption(
    "DESIGN AND ANALYSIS OF ALGORITHMS  /  PYTHON PROJECT"
)

st.divider()


# ==================== OVERVIEW ====================

if page == "Overview":

    st.subheader("Performance Overview")

    st.write(
        "A practical platform to study sorting and searching "
        "algorithms, compare execution times, visualize algorithm "
        "steps and understand theoretical time complexity."
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Algorithms", "5")
    c2.metric("Analysis Modules", "2")
    c3.metric("Visualization", "Interactive")

    st.markdown("### Algorithm Modules")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🔀 Sorting Algorithms")

        st.markdown("""
        - **Bubble Sort:** O(n²) average
        - **Merge Sort:** O(n log n)
        - **Quick Sort:** O(n log n) average
        """)

        st.caption(
            "Compare execution times and observe sorting operations."
        )

    with col2:
        st.markdown("#### 🔎 Searching Algorithms")

        st.markdown("""
        - **Linear Search:** O(n) average
        - **Binary Search:** O(log n) average
        """)

        st.caption(
            "Compare searching performance on sorted datasets."
        )

    st.markdown("### Getting Started")

    st.write(
        "Use the sidebar to run benchmarks, explore algorithm "
        "complexities or open the step-by-step Bubble Sort visualizer."
    )

    if st.session_state.results:
        df = pd.DataFrame(st.session_state.results)

        st.markdown("### Recent Benchmark Data")

        st.dataframe(
            df.tail(10),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "No benchmark results yet. Start with Sorting Analysis "
            "or Searching Analysis."
        )


# ==================== SORTING ANALYSIS ====================

elif page == "Sorting Analysis":

    st.subheader("🔀 Sorting Algorithm Benchmark")

    st.write(
        "Measure the execution time of three sorting algorithms "
        "across different input sizes."
    )

    max_size = st.select_slider(
        "Maximum dataset size",
        options=[500, 1000, 2000, 3000, 5000],
        value=2000
    )

    sizes = [
        n for n in [100, 300, 500, 1000, 2000, 3000, 5000]
        if n <= max_size
    ]

    selected = st.multiselect(
        "Select sorting algorithms",
        ["Bubble Sort", "Merge Sort", "Quick Sort"],
        default=["Bubble Sort", "Merge Sort", "Quick Sort"]
    )

    if st.button("▶ Run Sorting Benchmark", type="primary"):

        if not selected:
            st.warning("Select at least one algorithm.")

        else:
            benchmark_results = []
            progress = st.progress(0)

            total = len(sizes) * len(selected)
            completed = 0

            try:
                for size in sizes:

                    data = [
                        random.randint(0, 100000)
                        for _ in range(size)
                    ]

                    algorithms = {
                        "Bubble Sort": bubble_sort,
                        "Merge Sort": merge_sort,
                        "Quick Sort": quick_sort
                    }

                    for name in selected:
                        elapsed = time_sort(
                            algorithms[name],
                            data
                        )

                        benchmark_results.append({
                            "Category": "Sorting",
                            "Algorithm": name,
                            "Input Size": size,
                            "Time (ms)": elapsed
                        })

                        completed += 1
                        progress.progress(completed / total)

                st.session_state.results = [
                    r for r in st.session_state.results
                    if r["Category"] != "Sorting"
                ] + benchmark_results

                st.success(
                    "Sorting benchmark completed successfully!"
                )

            except Exception as error:
                st.error(f"Benchmark error: {error}")

    current = [
        r for r in st.session_state.results
        if r["Category"] == "Sorting"
    ]

    if current:

        df = pd.DataFrame(current)

        st.markdown("### Execution Time Comparison")

        fig = px.line(
            df,
            x="Input Size",
            y="Time (ms)",
            color="Algorithm",
            markers=True,
            template="plotly_dark",
            title="Sorting Execution Time vs Input Size"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0)",
            legend_title="Algorithm",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("### Benchmark Results")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download Sorting Results",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="sorting_results.csv",
            mime="text/csv"
        )


# ==================== ALGORITHM VISUALIZER ====================

elif page == "Algorithm Visualizer":

    st.subheader("🎬 Bubble Sort Visualizer")

    st.write(
        "Observe how Bubble Sort compares adjacent elements "
        "and swaps them step by step."
    )

    st.markdown("### Generate Your Dataset")

    size = st.slider(
        "Number of elements",
        min_value=5,
        max_value=15,
        value=8,
        key="visual_array_size"
    )

    if st.button("🎲 Generate New Array", type="primary"):

        values = random.sample(range(10, 100), size)

        st.session_state.visual_values = values
        st.session_state.visual_steps = create_bubble_steps(values)

        st.session_state.visual_generation += 1

        st.session_state.visual_step = 0

    if st.session_state.visual_steps:

        steps = st.session_state.visual_steps

        step_number = st.slider(
            "Move through sorting steps",
            min_value=0,
            max_value=len(steps) - 1,
            value=min(
                st.session_state.get("visual_step", 0),
                len(steps) - 1
            ),
            key=f"visual_step_{st.session_state.visual_generation}"
        )

        st.session_state.visual_step = step_number

        current = steps[step_number]

        arr = current["array"]
        left = current["left"]
        right = current["right"]

        colors = [
            "#F59E0B"
            if index in (left, right) and left >= 0
            else "#38BDF8"
            for index in range(len(arr))
        ]

        chart_data = pd.DataFrame({
            "Index": list(range(len(arr))),
            "Value": arr,
            "Bar Color": colors
        })

        fig = px.bar(
            chart_data,
            x="Index",
            y="Value",
            color="Bar Color",
            color_discrete_map="identity",
            text="Value",
            template="plotly_dark",
            title="Bubble Sort — Step-by-Step Visualization"
        )

        fig.update_layout(
            showlegend=False,
            xaxis_title="Array Index",
            yaxis_title="Element Value",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0)",
            transition_duration=250
        )

        fig.update_traces(
            textposition="outside",
            marker_line_width=0
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.info(
            f"Step {step_number + 1} of {len(steps)}: "
            f"{current['message']}"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric("Array Elements", len(arr))
        col2.metric("Current Step", step_number + 1)

        col3.metric(
            "Status",
            "Completed"
            if step_number == len(steps) - 1
            else "In Progress"
        )

        st.markdown("### Array State")

        st.write("**Current array:**", arr)

        st.write(
            "**Expected sorted array:**",
            sorted(st.session_state.visual_values)
        )

        st.caption(
            "Blue bars represent other elements. Orange bars "
            "highlight the two elements currently being compared."
        )

        col_prev, col_next = st.columns(2)

        with col_prev:
            if st.button(
                "⬅ Previous Step",
                disabled=(step_number == 0),
                use_container_width=True
            ):
                st.session_state.visual_step = step_number - 1
                st.rerun()

        with col_next:
            if st.button(
                "Next Step ➡",
                disabled=(step_number == len(steps) - 1),
                use_container_width=True
            ):
                st.session_state.visual_step = step_number + 1
                st.rerun()

    else:
        st.info(
            "Click Generate New Array to start the visualization."
        )


# ==================== SEARCHING ANALYSIS ====================

elif page == "Searching Analysis":

    st.subheader("🔎 Searching Algorithm Benchmark")

    st.write(
        "Compare Linear Search and Binary Search on sorted datasets. "
        "The target is placed at the last index to demonstrate "
        "a worst-case-style Linear Search."
    )

    max_size = st.select_slider(
        "Maximum dataset size",
        options=[1000, 5000, 10000, 50000, 100000],
        value=10000
    )

    sizes = [
        n for n in [1000, 5000, 10000, 50000, 100000]
        if n <= max_size
    ]

    if st.button("▶ Run Searching Benchmark", type="primary"):

        benchmark_results = []
        progress = st.progress(0)

        total = len(sizes) * 2
        completed = 0

        for size in sizes:

            data = list(range(size))
            target = size - 1

            algorithms = {
                "Linear Search": linear_search,
                "Binary Search": binary_search
            }

            for name, function in algorithms.items():

                elapsed = time_search(
                    function,
                    data,
                    target
                )

                benchmark_results.append({
                    "Category": "Searching",
                    "Algorithm": name,
                    "Input Size": size,
                    "Time (ms)": elapsed
                })

                completed += 1
                progress.progress(completed / total)

        st.session_state.results = [
            r for r in st.session_state.results
            if r["Category"] != "Searching"
        ] + benchmark_results

        st.success(
            "Searching benchmark completed successfully!"
        )

    current = [
        r for r in st.session_state.results
        if r["Category"] == "Searching"
    ]

    if current:

        df = pd.DataFrame(current)

        fig = px.line(
            df,
            x="Input Size",
            y="Time (ms)",
            color="Algorithm",
            markers=True,
            template="plotly_dark",
            title="Searching Execution Time vs Input Size"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15,23,42,0)",
            hovermode="x unified"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download Searching Results",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="searching_results.csv",
            mime="text/csv"
        )


# ==================== COMPLEXITY GUIDE ====================

elif page == "Complexity Guide":

    st.subheader("📘 Algorithm Complexity Reference")

    st.write(
        "Big-O notation describes how the resource requirements "
        "of an algorithm grow as the input size increases."
    )

    complexity_data = [
        ["Bubble Sort", "O(n)", "O(n²)", "O(n²)", "No"],
        [
            "Merge Sort",
            "O(n log n)",
            "O(n log n)",
            "O(n log n)",
            "No"
        ],
        [
            "Quick Sort",
            "O(n log n)",
            "O(n log n)",
            "O(n²)",
            "No"
        ],
        ["Linear Search", "O(1)", "O(n)", "O(n)", "No"],
        ["Binary Search", "O(1)", "O(log n)", "O(log n)", "Yes"]
    ]

    complexity_df = pd.DataFrame(
        complexity_data,
        columns=[
            "Algorithm",
            "Best Case",
            "Average Case",
            "Worst Case",
            "Sorted Input Required"
        ]
    )

    st.dataframe(
        complexity_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### Understanding Big-O")

    st.markdown("""
    - **O(1):** Constant time.
    - **O(log n):** Logarithmic growth.
    - **O(n):** Linear growth.
    - **O(n log n):** Common efficient sorting growth.
    - **O(n²):** Quadratic growth.
    """)

    st.markdown("### Algorithm Notes")

    st.markdown("""
    - Bubble Sort's best case is O(n) when the optimized algorithm
      detects an already sorted array.
    - Merge Sort guarantees O(n log n) time in all three cases.
    - Quick Sort has O(n²) worst-case time.
    - Linear Search checks elements sequentially.
    - Binary Search repeatedly halves the search interval and
      requires sorted input.
    """)

    st.warning(
        "Measured runtime depends on hardware, input distribution, "
        "Python implementation and system load. Big-O describes "
        "growth, not exact execution time."
    )


# ==================== RESULTS AND EXPORT ====================

elif page == "Results & Export":

    st.subheader("📈 Benchmark Results")

    if st.session_state.results:

        df = pd.DataFrame(st.session_state.results)

        col1, col2, col3 = st.columns(3)

        col1.metric("Measurements", len(df))
        col2.metric("Categories", df["Category"].nunique())
        col3.metric("Algorithms Tested", df["Algorithm"].nunique())

        st.markdown("### All Measurements")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "⬇ Download All Results (CSV)",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="algorithm_benchmark_results.csv",
            mime="text/csv"
        )

        if st.button("Clear All Results"):

            st.session_state.results = []
            st.rerun()

    else:

        st.info(
            "No results available yet. Run a sorting or searching "
            "benchmark first."
        )


# ==================== END OF APPLICATION ====================
