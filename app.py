import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from streamlit_extras import F
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer
from streamlit_timeline import timeline
from streamlit_image_select import image_select
import numpy as np
import math
import os
import plotly.graph_objects as go
import scipy.stats as stats
from scipy.stats import t
from scipy.stats import chi2_contingency
import plotly.figure_factory as ff


icon_page = Image.open("image/icon_page.png")
st.set_page_config("DataApp",icon_page,layout="wide",initial_sidebar_state="expanded",)

container = st.container()

def footer():
    st.markdown(
        """
        <head>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        </head>
        <style>
            footer
            {
            visibility:hidden;
            }
            .a {
                
                background-color: #f0f2f6;
                padding: 20px;
                text-align: center;
            }
            
            .icon-list {
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .icon-list-item {
                margin: 10px;
                text-align: center;
                cursor: pointer;
            }

            .icon-list-item i {
                display: block;
                font-size: 20px;
                color: black;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
    """
        <div class="a">
            <h6>Liên hệ với tôi</h6>
            <div class="icon-list">
                <div class="icon-list-item">
                    <a href="https://github.com" target="_blank">
                        <i class="fab fa-github"></i>
                    </a>
                </div>
                <div class="icon-list-item">
                    <a href="https://twitter.com" target="_blank">
                        <i class="fab fa-twitter"></i>
                    </a>
                </div>
                <div class="icon-list-item">
                    <a href="https://youtube.com" target="_blank">
                        <i class="fab fa-youtube"></i>
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
)

def search():
    st.markdown("""
            <head>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
            <style>
                body {
                font-family: Sans serif;
                }

                * {
                box-sizing: border-box;
                }

                form.example input[type=text] {
                padding: 10px;
                font-size: 17px;
                border: 2px solid white;
                float: left;
                width: 700px;  /* Set width to 100px */
                background: #f1f1f1;
                border-radius: 15px;
                }

                form.example button {
                float: left;
                width: 100px;  /* Set width to auto to adjust based on content */
                padding: 10px;
                background: #FF4B4B;
                color: white;
                font-size: 17px;
                border: 2px solid white;
                border-left: none;
                cursor: pointer;
                border-radius: 15px;
                }

                form.example button:hover {
                background: #FF4B4B;
                }

                form.example::after {
                content: "";
                clear: both;
                display: table;
                }
            </style>
            </head>
            <body>
            """, 
            unsafe_allow_html=True)

    st.markdown("""
            <form class="example" action="" style="margin:auto;max-width:800px">
            <input type="text" placeholder="Search.." name="search2">
            <button type="submit"><i class="fa fa-search"></i></button>
            </form>""",
            unsafe_allow_html=True)
    st.markdown(
                """
                <head>
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">
                </head>
                """,
                unsafe_allow_html=True
            )


    

@st.cache_data
def load_data(file):
    file_extension = os.path.splitext(file.name)[1].lower()
    if file_extension == '.csv':
        return pd.read_csv(file)
    elif file_extension in ['.xlsx', '.xls']:
        return pd.read_excel(file)



def summary(df):
    summary = df.describe()
    var_row = pd.Series(data=df.var(), name='var')
    var_row.index = summary.columns
    summary = pd.concat([summary.loc[['count', 'mean'], :], var_row.to_frame().T, summary.loc[['std', 'min', '25%', '50%', '75%', 'max'], :]])
    summary.loc['skew'] = df.skew()
    return summary

def summary_p(df):
    n = df.shape[0]
    summary = df.describe()
    var_row = pd.Series(data=df.var(), name='var')*((n-1)/n)
    var_row.index = summary.columns
    summary = pd.concat([summary.loc[['count', 'mean'], :], var_row.to_frame().T, summary.loc[['std', 'min', '25%', '50%', '75%', 'max'], :]])
    summary.loc['std'] = df.std()*math.sqrt((n-1)/n)
    summary.loc['skew'] = df.skew()*((n-2)/math.sqrt(n*(n-1)))
    return summary

   

def info(data):
    container.write(" # Thông tin dữ liệu # ")
    container.write("#### Dữ liệu ####")
    filtered_df = dataframe_explorer(data, case=False)
    container.dataframe(filtered_df, use_container_width=True)
    st.download_button(
            label="Download filter data",
            data=filtered_df.to_csv(index=False),
            file_name='data_filter.csv',
            mime='text/csv',
            )
    container.markdown("---")

    container.write("#### Thông tin ####")
    r=data.shape[0]
    c=data.shape[1]
    container.markdown(f"Kích thước dữ liệu: :red[{r}] x :red[{c}]")
    
    col1,col2,col3 = st.columns(3)


    with col1:
          
       st.write("Tên cột: ")
       st.dataframe(data.columns,use_container_width=True)
    with col2:
          
       st.write("Kiểu dữ liệu cột: ")
       st.dataframe(data.dtypes,use_container_width=True)
        
    with col3:
       st.write("Unique Values: ")
       st.dataframe(data.nunique(),use_container_width=True)

    container.markdown("---")
    st.markdown("#### Missing Values ####")
    col1n,col2n = st.columns([1,3])
    with col1n:   
        st.dataframe(data.isnull().sum(),use_container_width=True)
    with col2n:
        st.markdown("   Missing value (giá trị thiếu) trong khoa học dữ liệu và phân tích dữ liệu là giá trị không tồn tại hoặc không được xác định trong tập dữ liệu.")
        st.markdown("Missing value có thể xảy ra khi dữ liệu bị mất hoặc bị lỗi trong quá trình thu thập hoặc nhập liệu, hoặc có thể do một giá trị không có ý nghĩa được đại diện bởi các giá trị như NaN (Not a Number) hoặc NULL trong các ngôn ngữ lập trình.")
        data.dropna(inplace=True)
        data.reset_index(drop=True, inplace=True)
        st.download_button(
            label="Download clean data",
            data=data.to_csv(index=False),
            file_name='data_clean.csv',
            mime='text/csv',
            )
        container.markdown("---")
    footer()



### analyze_data      
def analyze_data(data):
    # Perform basic data analysis
    container.write(" # Data Analysis # ")
    container.write("#### Dữ liệu ####")
    container.write("Data")
    with container.expander("See explanation"):
        edited_df = container.data_editor(data,use_container_width=True,num_rows="dynamic")
    container.markdown("---")
    ######
    container.write("#### Thống kê mô tả một chiều ####")

    container.markdown("###### Bảng giá trị thống kê mô tả ######")
    use_sample_stats = st.checkbox('Hiệu chỉnh mẫu thống kê', value=True)
    if use_sample_stats:
    # compute and show the sample statistics
        container.dataframe(summary(edited_df),use_container_width=True)
        container.download_button(
        label="Download data as CSV",
        data=summary(data).to_csv(index=False),
        file_name='data_analyze.csv',
        mime='text/csv')
   
    else:
    # compute and show the population statistics
        container.dataframe(summary_p(edited_df),use_container_width=True)
        container.download_button(
        label="Download data as CSV",
        data=summary_p(data).to_csv(index=False),
        file_name='data_analyze.csv',
        mime='text/csv')
    

    container.markdown("---")
    container.markdown("###### Giá trị trung bình (Mean) ######")
    container.markdown("Giá trị trung bình, hay còn gọi là kỳ vọng, là một khái niệm thống kê dùng để đo độ trung tâm của một tập dữ liệu. Nó được tính bằng cách lấy tổng của tất cả các giá trị trong tập dữ liệu và chia cho số lượng các giá trị đó.")
    container.latex(r'''
    \operatorname{E}(X) = \frac{x_1 + x_2 + \dots + x_n}{n}
    ''')

    input1 = st.text_input("Ví dụ giá trị trung bình:",placeholder="Vd:1,2,4,2,5")


    values = input1.split(',')


    numeric_values = []
    for value in values:
        value = value.strip()
        if value:
            numeric_values.append(float(value))


    series1 = pd.Series(numeric_values)


    series1_mean = series1.mean()

    if input1:
        container.markdown(f"Giá trị trung bình của dãy: <span style='color:green;'>{series1_mean}</span>", unsafe_allow_html=True)
    container.markdown("---")

    container.markdown("###### Phương sai (Variance) ######")
    container.markdown("Phương sai (variance) là một thước đo về mức độ phân tán của các giá trị trong một tập dữ liệu. Nó đo lường độ lệch của mỗi giá trị so với giá trị trung bình của tập dữ liệu đó. Phương sai được tính bằng cách lấy tổng bình phương của hiệu giữa mỗi giá trị và giá trị trung bình, chia cho số lượng các giá trị trong tập dữ liệu.")
    container.latex(r'''
    \operatorname{Var}(X) = \sigma^2 = \frac{1}{N} \sum_{i=1}^N (x_i - \mu)^2
    ''')
    container.markdown("Phương sai mẫu hiệu chỉnh được tính bằng cách lấy tổng bình phương của hiệu giữa mỗi giá trị và giá trị trung bình, chia cho số lượng các giá trị trong mẫu trừ 1.")
    container.latex(r'''
    \operatorname{s}^2 = \frac{1}{n-1} \sum_{i=1}^n (x_i - \bar{x})^2
    ''')
    input2 = st.text_input("Ví dụ phương sai:",placeholder="Vd:1,2,4,2,5")
    values2 = input2.split(',')
    numeric_values1 = []
    for value in values2:
        value = value.strip()
        if value:
            numeric_values1.append(float(value))
    series2 = pd.Series(numeric_values1)
    series2_var = series2.var()
    if input1:
        container.markdown(f"Giá trị phương sai hiệu chỉnh của dãy: <span style='color:green;'>{series2_var}</span>", unsafe_allow_html=True)
    container.markdown("---")

    container.markdown("###### Các tứ phân vị (Quartiles) ######")
    container.markdown("Các tứ phân vị (quartiles) là một phương pháp thống kê mô tả để phân chia một tập dữ liệu thành bốn phần bằng nhau. Các tứ phân vị chia tập dữ liệu thành ba khoảng giá trị, được đánh số từ Q1 đến Q3, sao cho khoảng giá trị giữa Q1 và Q3 chứa 50% dữ liệu và khoảng giá trị giữa Q2 (tức là giá trị trung vị) cũng chứa 50% dữ liệu.")
    container.markdown("Tứ phân vị thứ nhất (Q1) tương ứng với phân vị 25%. Nó là giá trị mà có 25% dữ liệu nhỏ hơn hoặc bằng nó và 75% dữ liệu lớn hơn hoặc bằng nó.")
    container.latex(r'''
     \operatorname{Q1} =\begin{cases} x_{(\frac{n+1}{4})}, & \text{n là số chẵn} \\ \frac{1}{2}(x_{(\frac{n+1}{4})} + x_{(\frac{n+3}{4})}), & \text{n là số lẻ} \end{cases}
    ''')
    container.markdown("Tứ phân vị thứ hai (Q2) tương ứng với phân vị 50% hoặc giá trị trung vị. Nó là giá trị mà có 50% dữ liệu nhỏ hơn hoặc bằng nó và 50% dữ liệu lớn hơn hoặc bằng nó.")
    container.latex(r'''
     \operatorname{Q2} = \begin{cases} x_{(\frac{n+1}{2})}, & \text{n là số lẻ} \\ \frac{x_{(\frac{n}{2})} + x_{(\frac{n}{2}+1)}}{2}, & \text{n là số chẵn} \end{cases}
    ''')
    container.markdown("Tứ phân vị thứ ba (Q3) tương ứng với phân vị 75%. Nó là giá trị mà có 75% dữ liệu nhỏ hơn hoặc bằng nó và 25% dữ liệu lớn hơn hoặc bằng nó.")
    container.latex(r'''
     \operatorname{Q3} = \begin{cases} x_{(\frac{3n+1}{4})}, & \text{n là số chẵn} \\ \frac{1}{2}(x_{(\frac{3n+1}{4})} + x_{(\frac{3n+3}{4})}), & \text{n là số lẻ} \end{cases}
    ''')
    container.latex(r'''
    \textcolor{red}{\textbf{Chú ý: }} x_{(i)} \text{ là phần tử thứ $i$}  \text{ của tập dữ liệu đã được sắp xếp theo thứ tự tăng dần.}
    ''')
    #Eg 
    input3 = st.text_input("Ví dụ các tứ phân vị:",placeholder="Vd:1,2,4,2,5")
    values3 = input3.split(',')
    numeric_values3 = []
    for value3 in values3:
        value3 = value3.strip()
        if value3:
            numeric_values3.append(float(value3))
    series3 = pd.Series(numeric_values3)
    q1 = series3.quantile(0.25)
    q2 = series3.quantile(0.5)  # Median
    q3 = series3.quantile(0.75)
    if input3:
        container.markdown(f"Giá trị Q1: <span style='color:green;'>{q1}</span>", unsafe_allow_html=True)
        container.markdown(f"Giá trị Q2 (Trung vị): <span style='color:green;'>{q2}</span>", unsafe_allow_html=True)
        container.markdown(f"Giá trị Q3: <span style='color:green;'>{q3}</span>", unsafe_allow_html=True)
    container.markdown("---")

    
    container.markdown("###### Độ lệch (Skewness) ######")
    container.markdown("Skewness (độ lệch) là một độ đo thống kê được sử dụng để đo mức độ bất đối xứng của phân phối dữ liệu. Nó đo sự chệch lệch của phân phối dữ liệu so với phân phối chuẩn hoặc phân phối đối xứng")
    container.markdown("Nếu phân phối dữ liệu lệch sang phải (có đuôi phân phối dài hơn bên phải so với bên trái), thì giá trị skewness sẽ là số dương. Ngược lại, nếu phân phối dữ liệu lệch sang trái (có đuôi phân phối dài hơn bên trái so với bên phải), thì giá trị skewness sẽ là số âm. Nếu phân phối dữ liệu đối xứng, thì skewness sẽ bằng 0.")
    container.latex(r'''
    \operatorname{S} = \sqrt{n}\frac{\sum_{i=1}^N (x_i - \mu)^3}{\left(\sum_{i=1}^N (x_i - \mu)^2\right)^{3/2}}
    ''')
    container.markdown("Trong trường hợp muốn tính độ lệch skewness mẫu hiệu chỉnh ")
    container.latex(r'''
    \operatorname{S} = \frac{n\sqrt{n-1}}{n-2}\frac{\sum_{i=1}^N (x_i - \mu)^3}{\left(\sum_{i=1}^N (x_i - \mu)^2\right)^{3/2}}
    ''')
    input4 = st.text_input("Ví dụ skewness:",placeholder="Vd:1,2,4,2,5")
    values4 = input4.split(',')
    numeric_values4 = []
    for value4 in values4:
        value4 = value4.strip()
        if value4:
            numeric_values4.append(float(value4))
    series4 = pd.Series(numeric_values4)
    skewness = series4.skew()
    if input4:
        container.markdown(f"Giá trị skewness: <span style='color:green;'>{skewness}</span>", unsafe_allow_html=True)

    container.markdown("---")
    
    container.write("#### Đặc trưng thống kê mẫu nhiều chiều ####")
    container.markdown(
                """
                <style>
                .c {
                    margin-top: 30px ;
                    }
                </style>

                <div class="c"></div>
                """,
                unsafe_allow_html=True
            )
    col1,col2 = st.columns(2)
    with col1:
        col1.markdown("###### Ma trận hiệp phương sai ######")
        col1.dataframe(data.cov(),use_container_width=True)
    with col2:
        col2.markdown("######  Ma trận hệ số tương quan ######")
        col2.dataframe(data.corr(),use_container_width=True)
    container.markdown("#### Hiệp phương sai và hệ số tương quan ####")
    container.markdown("Ma trận hiệp phương sai là một ma trận đại diện cho phương sai của các biến ngẫu nhiên trong một tập dữ liệu đa chiều.")
    container.markdown("Ma trận hệ số tương quan là một phiên bản chuẩn hóa của ma trận hiệp phương sai. Nó cũng đại diện cho mối quan hệ giữa các biến trong tập dữ liệu đa chiều, nhưng thay vì hiển thị phương sai, nó hiển thị tương quan giữa các biến. Ma trận này được tính bằng cách chia mỗi phần tử trong ma trận hiệp phương sai cho tích của căn bậc hai của phương sai của hai biến tương ứng.")
    container.markdown("Công thức ma trận hiệp phương sai với phương sai mẫu hiệu chỉnh: ")
    container.latex(r'''
    \mathbf{S} = \frac{1}{n-1}(\mathbf{X}-\boldsymbol{\bar{X}})^T(\mathbf{X}-\boldsymbol{\bar{X}}) = 
        \begin{bmatrix}
            s_{11} & s_{12} & \cdots & s_{1n} \\
            s_{21} & s_{22} & \cdots & s_{2n} \\
            \vdots & \vdots & \ddots & \vdots \\
            s_{n1} & s_{n2} & \cdots & s_{nn}
        \end{bmatrix}

    ''')
    container.latex(r'''
    \text{Trong đó } s_{ij} = \frac{1}{n-1} \sum_{k=1}^{n} (x_{ki} - \bar{x_i})(x_{kj} - \bar{x_j})
    ''')
    container.markdown("Công thức hệ số tương quan: ")
    container.latex(r'''
    r_{XY} = \frac{\operatorname{cov}(X,Y)}{\sigma_X \sigma_Y}
    ''')
    container.markdown("ví dụ hiệp phương sai và hệ số tương quan: ")
    col1, col2 =st.columns(2)
    with col1:
        input5 = st.text_input("Input 1:", placeholder="Example: 1,2,3,4,5")
    with col2:
        input6 = st.text_input("Input 2:", placeholder="Example: 2,4,6,8,10")
    values5 = input5.split(',')
    numeric_values5 = []
    for value5 in values5:
        value5 = value5.strip()
        if value5:
            numeric_values5.append(float(value5))
    
    values6 = input6.split(',')
    numeric_values6 = []
    for value6 in values6:
        value6 = value6.strip()
        if value6:
            numeric_values6.append(float(value6))
    
    series5 = pd.Series(numeric_values5)
    series6 = pd.Series(numeric_values6)
    
    covariance = series5.cov(series6)
    correlation = series5.corr(series6)
    
    if input5 and input6:
        st.markdown(f"Giá trị hiệp phương sai: <span style='color:green;'>{covariance}</span>", unsafe_allow_html=True)
        st.markdown(f"Giá trị hệ số tương quan: <span style='color:green;'>{correlation}</span>", unsafe_allow_html=True)

    container.markdown("---")
    footer()


#### Data viusualyzation
def create_chart(chart_type, data):
    col1,col2 = st.columns(2)
    if chart_type == "Bar":
        
        st.header("Bar Chart")
        with col1:
            x_column = st.selectbox("Chọn trục X", data.columns)
        with col2:
            y_column = st.selectbox("Chọn trục Y", data.columns)
        fig = px.bar(data, x=x_column, y=y_column,color = x_column)
        st.plotly_chart(fig,theme=None, use_container_width=True)

    elif chart_type == "Line":
        st.header("Line Chart")
        multiple = st.checkbox("Vẽ nhiều đường", value=False)
        col1,col2 = st.columns(2)
        with col1:
            x_column = st.selectbox("Chọn trục X", data.columns)

        if multiple:
            container = st.empty()
            number = container.number_input("Nhập số lượng đường", min_value=1, step=1, value=1)
            with col2:
                y_columns = []
                for i in range(number):
                    with col2:
                        y_column = st.selectbox(f"Chọn trục Y {i+1}", data.columns)
                        y_columns.append(y_column)

    # Create line chart with multiple lines
            fig = px.line(data, x=x_column, y=y_columns, markers=True)

        else:
            with col2:
                y_column = st.selectbox("Chọn trục Y", data.columns)

        # Create line chart with single line
            fig = px.line(data, x=x_column, y=y_column, markers=True)

        st.plotly_chart(fig,theme=None, use_container_width=True)

    elif chart_type == "Scatter":

        st.header("Scatter Chart")
        col1,col2 = st.columns(2)
        with col1:
            x_column = st.selectbox("Chọn trục X", data.columns)
        with col2:
            y_column = st.selectbox("Chọn trục Y", data.columns)
        fig = px.scatter(data, x=x_column, y=y_column,color=x_column)
        st.plotly_chart(fig,theme=None, use_container_width=True)

    elif chart_type == "Pie":

        st.header("Biểu đồ tròn")
        col1,col2 = st.columns(2)
        with col1:
            x_column = st.selectbox("Chọn nhãn", data.columns)
        with col2:
            y_column = st.selectbox("Chọn giá trị", data.columns)
        donut = st.checkbox('Sử dụng donut', value=True)
        if donut:
        # compute and show the sample statistics
            hole = 0.4
   
        else:
         # compute and show the population statistics
            hole = 0
        fig = px.pie(data,names = x_column,values = y_column,hole=hole)
        st.plotly_chart(fig,theme=None, use_container_width=True)
    
    elif chart_type == "Boxplot":
        st.header("Biểu đồ Hộp")
        col1,col2 = st.columns(2)
        with col1:
            x_column = st.selectbox("Chọn trục X", data.columns)
        with col2:
            y_column = st.selectbox("Chọn trục Y", data.columns)

        fig = px.box(data,x = x_column,y = y_column, )
        st.plotly_chart(fig,theme=None, use_container_width=True)



#### hypothesis test
def hypothesis_test(test_type, data):
    # Perform basic data analysis
    
    ######
    if test_type =="Kiểm định một mẫu":
        container.markdown("---")
        container.write("#### Chọn phương thức kiểm định một mẫu mong muốn ####")
        test_type_one = st.selectbox("", ["Kiểm định về giá trị trung bình", "Kiểm định về phương sai"])
        if test_type_one=="Kiểm định về giá trị trung bình":
            container.markdown("---")
            container.write("#### Kiểm định về giá trị trung bình ####")
            container.markdown(
                """
                <style>
                .c {
                    margin-top: 30px ;
                    }
                </style>

                <div class="c"></div>
                """,
                unsafe_allow_html=True
            )
            container.write("##### Chọn cột cần kiểm định #####")
            numeric_columns = data.select_dtypes(include=["int", "float"]).columns
            x_column = st.selectbox("", numeric_columns)
            stats_df = pd.DataFrame({
                "Mean": [data[x_column].mean()],
                "Standard Deviation": [data[x_column].std()],
                "Count": [data[x_column].count()]
            })
                
            container.markdown("Giá trị thống kê tính được")
            reset_df=stats_df.set_index("Mean",drop=True)
            container.dataframe(reset_df,use_container_width=True)

            container.markdown("Các yếu tố: ")
            col1, col2, col3 = st.columns(3)
            with col1:
                clevel = st.text_input('Mức ý nghĩa', '0.05')
            with col2:
                a0 = st.text_input('Giá trị trung bình cần kiểm định', '')

            with col3:
                H1 = st.selectbox("Đối thuyết", ["Khác", "Lớn hơn", "Nhỏ hơn"])
            
            sample = data[x_column].values
            alpha = float(clevel)
            container.markdown("---")   
            

            if a0.strip():  # Check if a0 is not empty or whitespace
                container.markdown("###### Bài toán kiểm định giả thuyết:")
                col1, col2, col3 = st.columns(3)
                with col2:
                    if H1 == "Khác":
                        st.latex(r'''
                    \left\{
                    \begin{aligned}
                        H_0 &: \mu = \mu_0 \\
                        H_1 &: \mu \neq \mu_0
                    \end{aligned}
                    \right.
                    ''')
                    elif H1 == "Lớn hơn":
                        st.latex(r'''
                        \left\{
                        \begin{aligned}
                        H_0 &: \mu = \mu_0 \\
                        H_1 &: \mu > \mu_0
                    \end{aligned}
                        \right.
                        ''')
                    else:
                        st.latex(r'''
                        \left\{
                        \begin{aligned}
                        H_0 &: \mu = \mu_0 \\
                        H_1 &: \mu < \mu_0
                    \end{aligned}
                        \right.
                        ''')
                a0_value = float(a0)
                container.markdown("Thống kê phù hợp t:")
                container.latex(r'''
                t=\dfrac{(\overline{x}-\mu)\sqrt{n}}{s_d}
                ''')
                container.latex(r'''\text{Ta có: }
                t \sim t_{n-1}
                ''')

                if H1 == "Khác":
                    t_statistic, p_value= stats.ttest_1samp(sample, popmean=a0_value)
                    container.markdown(f"Giá trị $$t$$ tính được là: <span style='color: green'> $$t = {t_statistic}$$</span>", unsafe_allow_html=True)
                    percent=stats.t.ppf(q=1-alpha/2, df=data[x_column].count()-1)
                    t_critical_1 = t.ppf(alpha / 2, data[x_column].count()-1)
                    t_critical_2 = t.ppf(1 - alpha / 2, data[x_column].count()-1)

                    # Generate x values for the PDF plot
                    x = np.linspace(-5, 5, 1000)

                    # Calculate the PDF values
                    pdf = t.pdf(x, data[x_column].count()-1)

                    # Plot the PDF
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x, y=pdf, name="PDF"))
                    fig.update_layout(
                        title=f"Student's t-Distribution PDF (df={data[x_column].count()-1})",
                        xaxis_title="x",
                        yaxis_title="PDF",
                    )

                    x_fill1 = np.linspace(-5, t_critical_1, 1000)
                    pdf_fill1 = t.pdf(x_fill1, data[x_column].count()-1)

                    x_fill2 = np.linspace(t_critical_2, 5, 1000)
                    pdf_fill2 = t.pdf(x_fill2, data[x_column].count()-1)

                    # Highlight the area under the curve    
                    fig.add_trace(go.Scatter(x=x_fill1, y=pdf_fill1, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))
                    fig.add_trace(go.Scatter(x=x_fill2, y=pdf_fill2, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))

                    # Highlight the two tail areas
                    fig.add_trace(go.Scatter(x=[t_critical_1, t_critical_1], y=[0, t.pdf(t_critical_1, data[x_column].count()-1)],
                                mode="lines", name="Left Tail Area", line=dict(color="red", dash="dash")))
                    fig.add_trace(go.Scatter(x=[t_critical_2, t_critical_2], y=[0, t.pdf(t_critical_2, data[x_column].count()-1)],
                                mode="lines", name="Right Tail Area", line=dict(color="red", dash="dash")))

                    # Display the plot
                    st.plotly_chart(fig,theme=None, use_container_width=True)
                    
                    

                    inf = r"\infty"
                    hop = r"\cup"
                    st.markdown("##### Kết luận")
                    st.markdown(f"Miền bác bỏ hai phía ($$-{inf},{t_critical_1}$$) $${hop}$$ ($${t_critical_2},{inf}$$)")
                    if(np.abs(t_statistic) > percent):
                        latex_expression = r"t_{n-1}(\frac{\alpha}{2})"
                        st.markdown(f"Vì |t_statistic| = :green[{np.abs(t_statistic)}] > $$ {latex_expression}$$ = :green[{percent}] ")
                        st.markdown(f"Nên ta bác bỏ giả thuyết H0 ở mức ý nghĩa :green[{alpha}]")
                    else:
                        latex_expression = r"t_{n-1}(\frac{\alpha}{2})"
                        st.markdown(f"Vì |t_statistic|= :green[{np.abs(t_statistic)}] < $$ {latex_expression}$$=:green[{percent}] ")
                        st.markdown(f"Nên ta chấp nhận giả thuyết H0 ở mức ý nghĩa :green[{alpha}]")

                elif H1 == "Lớn hơn":
                    percent=stats.t.ppf(q=1-alpha, df=data[x_column].count()-1)
                    t_statistic = (data[x_column].mean() - a0_value) / (data[x_column].std() / math.sqrt(data[x_column].count()))
                    st.markdown(f"t-statistic= :green[{t_statistic}]")
                    t_critical = stats.t.ppf(1 - alpha, df=data[x_column].count()-1)

                    # Generate x values for the PDF plot
                    x = np.linspace(-5, 5, 1000)

                    # Calculate the PDF values
                    pdf = stats.t.pdf(x, df=data[x_column].count()-1)

                    # Plot the PDF
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x, y=pdf, name="PDF"))
                    fig.update_layout(
                    title=f"Student's t-Distribution PDF (df={data[x_column].count()-1})",
                    xaxis_title="x",
                    yaxis_title="PDF",
                    )

                    x_fill = np.linspace(t_critical, x[-1], 1000)
                    pdf_fill = stats.t.pdf(x_fill, df=data[x_column].count()-1)

                    # Highlight the area under the curve
                    fig.add_trace(go.Scatter(x=x_fill, y=pdf_fill, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))

                    # Highlight the critical region
                    fig.add_trace(go.Scatter(x=[t_critical, t_critical], y=[0, stats.t.pdf(t_critical, df=data[x_column].count()-1)],
                                mode="lines", name="Critical Region", line=dict(color="red", dash="dash")))


                    st.plotly_chart(fig, theme=None, use_container_width=True)
                    inf = r"\infty"
                    hop = r"\cup"
                    st.markdown("##### Kết luận")
                    st.markdown(f"Miền bác bỏ một phía ($$-{inf},{t_critical}$$) ")
                    if(t_statistic > percent):
                        latex_expression = r"t_{n-1}({1- \alpha})"
                        st.markdown(f"Vì t_statistic= :green[{t_statistic}] > $$ {latex_expression}$$ = :green[{percent}] ")
                        st.markdown(f"nên ta bác bỏ giả thuyết H0 ở mức ý nghĩa :green[{alpha}]")
                    else:
                        latex_expression = r"t_{n-1}({1- \alpha})"
                        st.markdown(f"Vì t_statistic= :green[{t_statistic}] < $$ {latex_expression}$$=:green[{percent}] ")
                        st.markdown(f"nên ta chấp nhận giả thuyết H0 ở mức ý nghĩa :green[{alpha}]")  
                else:
                    percent=stats.t.ppf(q=alpha, df=data[x_column].count()-1)
                    t_statistic = (data[x_column].mean() - a0_value) / (data[x_column].std() / math.sqrt(data[x_column].count()))
                    st.markdown(f"t-statistic= :green[{t_statistic}]")
                    t_critical = stats.t.ppf(alpha, df=data[x_column].count()-1)
                    # Generate x values for the PDF plot
                    x = np.linspace(-5, 5, 1000)

                    # Calculate the PDF values
                    pdf = stats.t.pdf(x, df=data[x_column].count()-1)

                    # Plot the PDF
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x, y=pdf, name="PDF"))
                    fig.update_layout(
                    title=f"Student's t-Distribution PDF (df={data[x_column].count()-1})",
                    xaxis_title="x",
                    yaxis_title="PDF",
                    )

                    x_fill = np.linspace(-5,t_critical, 1000)
                    pdf_fill = stats.t.pdf(x_fill, df=data[x_column].count()-1)

                    # Highlight the area under the curve
                    fig.add_trace(go.Scatter(x=x_fill, y=pdf_fill, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))

                    # Highlight the critical region
                    fig.add_trace(go.Scatter(x=[t_critical, t_critical], y=[0, stats.t.pdf(t_critical, df=data[x_column].count()-1)],
                                mode="lines", name="Critical Region", line=dict(color="red", dash="dash")))

                    st.plotly_chart(fig, theme=None, use_container_width=True)
                    inf = r"\infty"
                    hop = r"\cup"
                    st.markdown("##### Kết luận")
                    st.markdown(f"Miền bác bỏ một phía ($${t_critical},{inf}$$) ")
                    if(t_statistic < percent):
                        latex_expression = r"t_{n-1}({\alpha})"
                        st.markdown(f"Vì t_statistic= :green[{t_statistic}] < $$ {latex_expression}$$ = :green[{percent}] ")
                        st.markdown(f"nên ta bác bỏ giả thuyết H0 ở mức ý nghĩa :green[{alpha}]")
                    else:
                        latex_expression = r"t_{n-1}({\alpha})"
                        st.markdown(f"Vì t_statistic= :green[{t_statistic}] > $$ {latex_expression}$$=:green[{percent}] ")
                        st.markdown(f"nên ta chấp nhận giả thuyết H0 ở mức ý nghĩa :green[{alpha}]")  

        #
        if test_type_one=="Kiểm định về phương sai":
            container.write("#### Kiểm định về phương sai ####")
            numeric_columns = data.select_dtypes(include=["int", "float"]).columns
            x_column = st.selectbox("Chọn cột cần kiểm định ", numeric_columns)
            stats_df = pd.DataFrame({
                    "Variance": [data[x_column].var()],
                    "Count": [data[x_column].count()]
                })
                    
            container.markdown("Giá trị thống kê tính được")
            reset_df = stats_df.set_index("Variance", drop=True)
            container.dataframe(reset_df, use_container_width=True)
            container.markdown("Các yếu tố: ")
            col1, col2 = st.columns(2)
            with col1:
                clevel = st.text_input('Mức ý nghĩa', '0.05')
            with col2:
                a0 = st.text_input('Giá trị phương sai cần kiểm định', '')


            sample = data[x_column].values
            alpha = float(clevel)
            container.markdown("---")   

            if a0.strip():  # Check if a0 is not empty or whitespace
                container.markdown("###### Bài toán kiểm định giả thuyết:")
                col1, col2,col3 = st.columns(3)
                with col2:
                    st.latex(r'''
                    \left\{
                    \begin{aligned}
                        H_0 &: \sigma^2 = \sigma_0^2 \\
                        H_1 &: \sigma^2 \neq \sigma_0^2
                    \end{aligned}
                    \right.
                    ''')

                

                a0_value = float(a0)
                container.markdown("Thống kê phù hợp chi-square:")
                container.latex(r'''
                \chi^2 = (n-1) \cdot \frac{{s^2}}{{\sigma_0^2}}
                ''')
                container.latex(r'''\text{Ta có: }
                \chi^2 \sim \chi^2_{n-1}
                ''')
                
                
                chi2_statistic = (data[x_column].count() - 1) * data[x_column].var() / a0_value
                st.markdown(f"chi-square statistic = :green[{chi2_statistic}]")
                chi2_critical = stats.chi2.ppf(1 - alpha / 2, df=data[x_column].count() - 1)
                chi2_critical2 = stats.chi2.ppf(alpha / 2, df=data[x_column].count() - 1)

                # Generate x values for the Chi-square distribution plot
                x = np.linspace(stats.chi2.ppf(alpha / 2, df=data[x_column].count() - 1)-20, stats.chi2.ppf(1 - alpha / 2, df=data[x_column].count() - 1)+20, 1000)

                # Calculate the PDF values
                pdf = stats.chi2.pdf(x, df=data[x_column].count()-1)

                # Plot the PDF
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x, y=pdf, name="PDF"))
                fig.update_layout(
                    title=f"Chi-square Distribution PDF (df={data[x_column].count()-1})",
                    xaxis_title="x",
                    yaxis_title="PDF",
                )

                x_fill1 = np.linspace(x[0], chi2_critical2, 1000)
                pdf_fill1 = stats.chi2.pdf(x_fill1, df=data[x_column].count()-1)

                x_fill2 = np.linspace(chi2_critical,x[-1], 1000)
                pdf_fill2 = stats.chi2.pdf(x_fill2, df=data[x_column].count()-1)

                fig.add_trace(go.Scatter(x=x_fill1, y=pdf_fill1, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))
                fig.add_trace(go.Scatter(x=x_fill2, y=pdf_fill2, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))
                
                fig.add_trace(go.Scatter(x=[chi2_critical, chi2_critical], y=[0, stats.chi2.pdf(chi2_critical, data[x_column].count()-1)],
                                mode="lines", name="Left Tail Area", line=dict(color="red", dash="dash")))
                fig.add_trace(go.Scatter(x=[chi2_critical2, chi2_critical2], y=[0, stats.chi2.pdf(chi2_critical2, data[x_column].count()-1)],
                                mode="lines", name="Right Tail Area", line=dict(color="red", dash="dash")))
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,theme=None, use_container_width=True)
                
                if chi2_statistic > chi2_critical or chi2_statistic < chi2_critical2:
                    container.markdown(":red[Không chấp nhận null hypothesis]")
                    container.markdown("Có bằng chứng đủ để bác bỏ giả thuyết H0.")
                else:
                    container.markdown(":green[Chấp nhận null hypothesis]")
                    container.markdown("Không có bằng chứng đủ để bác bỏ giả thuyết H0.")
    if test_type =="Kiểm định nhiều mẫu":
        container.markdown("---")
        container.write("#### Chọn phương thức kiểm định nhiều mẫu mong muốn ####")
        test_type_two = st.selectbox("", ["So sánh hai giá trị trung bình", "So sánh hai phương sai", "Phân tích phương sai"])
        if test_type_two=="So sánh hai giá trị trung bình":
            container.markdown("---")
            container.write("#### So sánh hai giá trị trung bình ####")
            container.markdown(
                """
                <style>
                .c {
                    margin-top: 30px ;
                    }
                </style>

                <div class="c"></div>
                """,
                unsafe_allow_html=True
            )
            container.write("##### Chọn các cột cần so sánh #####")
            numeric_columns = data.select_dtypes(include=["int", "float"]).columns
            col1, col2  = st.columns(2)
            with col1:
                x_column = st.selectbox("Mẫu 1", numeric_columns)
            with col2:
                y_column = st.selectbox("Mẫu 2", numeric_columns)
            stats_df = pd.DataFrame({
                "Mẫu 1": [data[x_column].mean(), data[x_column].std(), data[x_column].count()],
                "Mẫu 2": [data[y_column].mean(), data[y_column].std(), data[y_column].count()]
            }, index=["Mean", "Standard Deviation", "Count"])
                
            container.markdown("Giá trị thống kê tính được")
            container.dataframe(stats_df, use_container_width=True)

            container.markdown("Các yếu tố: ")
            col1, col2  = st.columns(2)
            with col1:
                clevel = st.text_input('Mức ý nghĩa', '0.05')
            with col2:
                a0 = st.text_input('Giá trị cần so sánh', '')
            
            
            alpha = float(clevel)
            container.markdown("---")   
            

            if a0.strip():  # Check if a0 is not empty or whitespace
                container.markdown("###### Bài toán kiểm định giả thuyết:")
                col1, col2, col3 = st.columns(3)
                with col2:
                        st.latex(r'''
                        \left\{
                        \begin{aligned}
                        H_0 &: \mu_1 - \mu_2   = a_0 \\
                        H_1 &: \mu_1 - \mu_2   \neq a_0
                    \end{aligned}
                        \right.
                        ''')
                
                a0_value = float(a0)
                container.markdown("Thống kê phù hợp t:")
                if data[x_column].count() > 30:
                    container.latex(r'''
                    t=\frac{{\overline{x_1} - \overline{x_2}-(\mu_1 -\mu_2)}}{\sqrt{\frac{{s_1^2}}{{n_1}}+\frac{s_2^2}{{n_2}}}}
                    ''')
                    container.latex(r'''\text{Ta có: }
                    t \sim t_{min{(n_1-1, n_2-1)}}
                    ''')
                else:
                    container.latex(r'''
                    t=\frac{{\overline{x_1} - \overline{x_2}-(\mu_1 -\mu_2)}}{{\sqrt{\frac{{(n_1-1)s_1^2+(n_2-1)s_2^2}}{{n_1+n_2-2}}(\frac{{1}}{{n_1}}+\frac{1}{{n_2}})}}}
                    ''')
                    container.latex(r'''\text{Ta có: }
                    t \sim t_{n_1+n_2-2}
                    ''')
                t_statistic2 = (data[x_column].mean() - data[y_column].mean() - a0_value) / (math.sqrt((((data[x_column].count()-1)*data[x_column].var()+(data[y_column].count()-1)*data[y_column].var())/((data[x_column].count()+data[y_column].count()-2)))*(1/(data[x_column].count())+1/data[y_column].count())))
                st.markdown(f"t statistic = :green[{t_statistic2}]")
                t_critical_1 = t.ppf(alpha / 2, data[x_column].count()-1)
                t_critical_2 = t.ppf(1 - alpha / 2, data[x_column].count()-1)

                    # Generate x values for the PDF plot
                x = np.linspace(-5, 5, 1000)

                    # Calculate the PDF values
                pdf = t.pdf(x, data[x_column].count()+data[y_column].count()-2)

                    # Plot the PDF
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x, y=pdf, name="PDF"))
                fig.update_layout(
                        title=f"Student's t-Distribution PDF (df={data[x_column].count()+data[y_column].count()-2})",
                        xaxis_title="x",
                        yaxis_title="PDF",
                    )

                x_fill1 = np.linspace(-5, t_critical_1, 1000)
                pdf_fill1 = t.pdf(x_fill1, data[x_column].count()+data[y_column].count()-2)

                x_fill2 = np.linspace(t_critical_2, 5, 1000)
                pdf_fill2 = t.pdf(x_fill2, data[x_column].count()+data[y_column].count()-2)

                    # Highlight the area under the curve    
                fig.add_trace(go.Scatter(x=x_fill1, y=pdf_fill1, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))
                fig.add_trace(go.Scatter(x=x_fill2, y=pdf_fill2, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))

                    # Highlight the two tail areas
                fig.add_trace(go.Scatter(x=[t_critical_1, t_critical_1], y=[0, t.pdf(t_critical_1, data[x_column].count()+data[y_column].count()-2)],
                            mode="lines", name="Left Tail Area", line=dict(color="red", dash="dash")))
                fig.add_trace(go.Scatter(x=[t_critical_2, t_critical_2], y=[0, t.pdf(t_critical_2, data[x_column].count()+data[y_column].count()-2)],
                                mode="lines", name="Right Tail Area", line=dict(color="red", dash="dash")))

                    # Display the plot
                st.plotly_chart(fig,theme=None, use_container_width=True)
        if test_type_two =="So sánh hai phương sai":
            container.write("#### So sánh hai phương sai ####")
            numeric_columns = data.select_dtypes(include=["int", "float"]).columns
            col1,col2 = st.columns(2)
            with col1:
                x_column = st.selectbox("Mẫu 1 ", numeric_columns)
            with col2:
                y_column = st.selectbox("Mẫu 2", numeric_columns)
            stats_df = pd.DataFrame({
                "Mẫu 1": [ data[x_column].var(), data[x_column].count()],
                "Mẫu 2": [ data[y_column].var(), data[y_column].count()]
            }, index=["Variance", "Count"])

            container.markdown("Giá trị thống kê tính được")
            container.dataframe(stats_df, use_container_width=True)

            container.markdown("Các yếu tố: ")
            col1, col2 = st.columns(2)
            with col1:
                clevel = st.text_input('Mức ý nghĩa', '0.05')
            with col2:
                H1 = st.selectbox("Đối thuyết", ["Khác", "Lớn hơn", "Nhỏ hơn"])


            sample = data[x_column].values
            alpha = float(clevel)
            container.markdown("---")   

            if H1=="Khác":  # Check if a0 is not empty or whitespace
                container.markdown("###### Bài toán kiểm định giả thuyết:")
                col1, col2,col3 = st.columns(3)
                with col2:
                    st.latex(r'''
                    \left\{
                    \begin{aligned}
                        H_0 &: \sigma_1^2 = \sigma_2^2 \\
                        H_1 &: \sigma_1^2 \neq \sigma_2^2
                    \end{aligned}
                    \right.
                    ''')
                
                container.markdown("Thống kê phù hợp chi-square:")
                container.latex(r'''
                F = \frac{{s_1^2 \sigma_2^2}}{{s_2^2 \sigma_1^2}}
                ''')
                container.latex(r'''\text{Ta có: }
                F \sim F_{n_1-1,n_2-1}
                ''')
                
                
                F_statistic = (data[x_column].var())/ (data[y_column].var())
                st.markdown(f"chi-square statistic = :green[{F_statistic}]")
                F_critical = stats.f.ppf(1 - alpha / 2, data[x_column].count() - 1,data[y_column].count() - 1)
                F_critical2 = stats.f.ppf(alpha / 2, data[x_column].count() - 1,data[y_column].count() - 1)

                # Generate x values for the Chi-square distribution plot
                x = np.linspace(-2*F_critical2, 2*F_critical, 1000)

                # Calculate the PDF values
                pdf = stats.f.pdf(x, data[x_column].count() - 1,data[y_column].count() - 1)

                # Plot the PDF
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=x, y=pdf, name="PDF"))
                fig.update_layout(
                    title=f"F Distribution PDF (df={data[x_column].count()-1},{data[y_column].count()-1})",
                    xaxis_title="x",
                    yaxis_title="PDF",
                )

                x_fill1 = np.linspace(x[0], F_critical2, 1000)
                pdf_fill1 = stats.f.pdf(x_fill1, data[x_column].count() - 1,data[y_column].count() - 1)

                x_fill2 = np.linspace(F_critical,x[-1], 1000)
                pdf_fill2 = stats.f.pdf(x_fill2, data[x_column].count() - 1,data[y_column].count() - 1)

                fig.add_trace(go.Scatter(x=x_fill1, y=pdf_fill1, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))
                fig.add_trace(go.Scatter(x=x_fill2, y=pdf_fill2, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))
                
                fig.add_trace(go.Scatter(x=[F_critical, F_critical], y=[0, stats.f.pdf(F_critical, data[x_column].count() - 1,data[y_column].count() - 1)],
                                mode="lines", name="Left Tail Area", line=dict(color="red", dash="dash")))
                fig.add_trace(go.Scatter(x=[F_critical2, F_critical2], y=[0, stats.f.pdf(F_critical2, data[x_column].count() - 1,data[y_column].count() - 1)],
                                mode="lines", name="Right Tail Area", line=dict(color="red", dash="dash")))
                
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig,theme=None, use_container_width=True)

        if test_type_two =="Phân tích phương sai":
            container.write("#### ANOVA Test ####")

            container.write("##### Chọn các cột cho ANOVA #####")
            numeric_columns = data.select_dtypes(include=["int", "float"]).columns
            col1,col2 = st.columns([3,1])
            with col1:
                columns = st.multiselect("Select columns for ANOVA test", numeric_columns)
            with col2:
                clevel = st.text_input('Mức ý nghĩa', '0.05')
            alpha = float(clevel)
            if len(columns) > 1:
    # Filter the DataFrame to include only the selected columns
                selected_data = data[columns]

                # Convert each column to a Series and drop NaN values
                series_data = []
                for col in columns:
                    series = selected_data[col].dropna()
                    series_data.append(series)
                
                if len(series_data) > 1:
                    # Perform the ANOVA analysis
                    summary_table = pd.DataFrame(columns=["Column", "Mean", "Standard Deviation", "Count"])
                    for i, col in enumerate(columns):
                        summary_table = summary_table.append({
                            "Column": col,
                            "Mean": series_data[i].mean(),
                            "Standard Deviation": series_data[i].std(),
                            "Count": series_data[i].count()
                        }, ignore_index=True)
                    # Display the column summaries in Streamlit
                    container.write("#### Giá trị thống kê tính được ####")
                    container.dataframe(summary_table, use_container_width=True)
                    f_statistic, p_value = stats.f_oneway(*series_data)
                    within_squares = sum(sum((series - series.mean())**2) for series in series_data)
                    overall_mean = pd.Series(selected_data.values.flatten()).dropna().mean()
                    between_squares = sum(len(series) * (series.mean() - overall_mean)**2 for series in series_data)
                    total_squares = within_squares + between_squares
                        
                    # Create the ANOVA table
                    anova_table = pd.DataFrame({
                        "Nguồn biến thiên": ["Xử lý", "Phần dư", "Tổng cộng"],
                        "Tổng bình phương": [
                            between_squares,
                            within_squares,
                            total_squares
                        ],
                            
                        "Bậc tự do": [
                            len(series_data) - 1,
                            sum(len(series) - 1 for series in series_data),
                            sum(len(series) for series in series_data) - 1
                        ],
                        "Tỉ số MS": [
                            between_squares / (len(series_data) - 1),
                            within_squares / sum(len(series) - 1 for series in series_data),
                            ""
                        ],
                        "F-Value": [
                            "",
                            f_statistic,
                            ""
                        ],
                        "p-value": [
                            "",
                            p_value,
                            ""
                        ]
                    })

                    # Display the ANOVA table in Streamlit
                    container.write("#### Bảng ANOVA ####")
                    container.dataframe(anova_table, use_container_width=True)

                    F_critical = stats.f.ppf(1 - alpha , (len(series_data) - 1),sum(len(series) - 1 for series in series_data))
                    

                    # Generate x values for the Chi-square distribution plot
                    x = np.linspace(0, 2*F_critical, 1000)

                    # Calculate the PDF values
                    pdf = stats.f.pdf(x, (len(series_data) - 1),sum(len(series) - 1 for series in series_data))

                    # Plot the PDF
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(x=x, y=pdf, name="PDF"))
                    fig.update_layout(
                        title=f"F Distribution PDF (df={(len(series_data) - 1)},{sum(len(series) - 1 for series in series_data)})",
                        xaxis_title="x",
                        yaxis_title="PDF",
                    )

                    
                    x_fill2 = np.linspace(F_critical,x[-1], 1000)
                    pdf_fill2 = stats.f.pdf(x_fill2, (len(series_data) - 1),sum(len(series) - 1 for series in series_data))


                    fig.add_trace(go.Scatter(x=x_fill2, y=pdf_fill2, fill='tozeroy', fillcolor='rgba(100, 10, 10, 0.3)',
                                    mode='lines', line=dict(color='rgba(0, 0, 0, 0)'), name='Area Under Curve'))
                    
                    fig.add_trace(go.Scatter(x=[F_critical, F_critical], y=[0, stats.f.pdf(F_critical, (len(series_data) - 1),sum(len(series) - 1 for series in series_data))],
                                    mode="lines", name="Left Tail Area", line=dict(color="red", dash="dash")))
                    
                    
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig,theme=None, use_container_width=True)
                else:
                    container.write("Insufficient data points after preprocessing. Please select columns with valid numeric values.")
            else:
                container.write("Please select at least two columns for the ANOVA test.")


    if test_type =="Kiểm định phi tham số":
        container.markdown("---")
        container.write("#### Chọn phương thức kiểm định mong muốn ####")
        test_type_three = st.selectbox("", ["Kiểm định phân phối chuẩn"])
        if test_type_three == "Kiểm định phân phối chuẩn":
            numeric_columns = data.select_dtypes(include=["int", "float"]).columns
            column = st.selectbox("Select a Column", numeric_columns)
            sort_col = data[column].sort_values().reset_index(drop=True)

            # Calculate z-scores for the selected column
            z_scores = (sort_col.index + 1 - 0.5) / len(data[column])

            # Generate theoretical quantiles
            quantiles = np.linspace(sort_col[0], sort_col[5], len(data[column]))
            theoretical_quantiles = stats.norm.ppf(z_scores)

            # Create the QQ plot
            qq_fig = go.Figure()
            qq_fig.add_trace(go.Scatter(x=sort_col, y=theoretical_quantiles, mode="markers", name="QQ Plot"))

            # Add linear regression line
            slope, intercept, _, _, _ = stats.linregress(sort_col, theoretical_quantiles)
            regression_line = intercept + slope * sort_col
            qq_fig.add_trace(go.Scatter(x=sort_col, y=regression_line, mode="lines", name="Linear",line=dict(color='red')))

            qq_fig.update_layout(
                title=f"Biểu đồ Q-Q plot",
                xaxis_title="Sample Quantiles",
                yaxis_title="Theoretical Quantiles",
            )
            
            
            

            # Display the QQ plot
            
            
            container.plotly_chart(qq_fig,theme = None, use_container_width=True)
            
            container.write(np.corrcoef(sort_col, theoretical_quantiles))


        
       
# main function
def main():

    image = Image.open("logo_app.png")
    with st.sidebar:
        st.sidebar.image(image,width = 250)
        st.sidebar.markdown("---")
        st.markdown("#### Chọn chức năng ####")
        selected = option_menu(None, ["Dữ liệu", "Thống kê", "Trực quan hóa","Kiểm định","Hoi quy"], 
            icons=['clipboard-data', 'table', "bar-chart-fill", 'clipboard-check'], 
            menu_icon="cast", default_index=0,styles={
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "black", "font-size": "15px"},
                                   "nav-link": {"font-size": "15px", "text-align": "left", "margin": "0px",
                                                "--hover-color": "#eee"},
                                   })

    with container:
        with st.sidebar:
            st.sidebar.markdown("---")
            st.markdown("#### Tải lên dữ liệu ####")
            file = st.file_uploader("",type=["csv", "xlsx", "xls"])

        if file is not None:

            data = load_data(file)

            if selected =='Dữ liệu':
                search()
                info(data)

            if selected == 'Thống kê':
                search()
                analyze_data(data)

            if selected =='Trực quan hóa':
                search()
                container.write(" # Trực quan hóa dữ liệu # ")
                container.write("#### Dữ liệu ####")
                container.write("Data")
                edit_data= container.data_editor(data,use_container_width=True,num_rows="dynamic")
                container.markdown("---")
                container.write("#### Chọn loại biểu đồ ####")
                chart_type = st.selectbox("", ["Bar", "Line", "Scatter","Pie","Boxplot"])

                create_chart(chart_type, edit_data)

            if selected =='Kiểm định':
                search()
                container.write(" # Kiểm định giả thuyết thống kê # ")
                container.write("#### Dữ liệu ####")
                container.write("Data")
                edit_data= container.data_editor(data,use_container_width=True,num_rows="dynamic")
                container.markdown("---")
                container.write("#### Chọn phương thức muốn kiểm định ####")
                test_type = st.selectbox("", [None,"Kiểm định một mẫu", "Kiểm định nhiều mẫu", "Kiểm định phi tham số"])
                hypothesis_test(test_type, edit_data)
        else:
            
            with container:
                with st.spinner(text="Building line"):
                        with open('timeline.json', "r",encoding="utf-8") as f:
                            data = f.read()
                            timeline(data, height=450, )
            container.markdown("---")
           
            st.markdown(
                """
                <style>
                .b {
                    margin-top: 50px ;
                    }
                </style>

                <div class="b"></div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(" ### Làm sao để sử dụng ?")
            st.markdown(
                """
                <style>
                .b {
                    margin-top: 50px ;
                    }
                </style>

                <div class="b"></div>
                """,
                unsafe_allow_html=True
            )

            col1,col2=st.columns(2)
            with col1:
                st.markdown("""
                        <head>
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                        </head>
                        <body>

                        <i class="fa-solid fa-1 fa-beat" style="font-size:70px;color: #ff4b4b;"></i>
                        <h5>Tải lên dữ liệu của bạn</h5>
                        </body>
                                            
                        
                        """, unsafe_allow_html=True)
                image1 = Image.open("image/im1.png")
                st.image(image1)

                st.markdown(
                """
                <style>
                .b {
                    margin-top: 50px ;
                    }
                </style>

                <div class="b"></div>
                """,
                unsafe_allow_html=True
            )
                st.markdown("""
                        <head>
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                        </head>
                        <body>

                        <i class="fa-solid fa-3 fa-beat" style="font-size:70px;color: #ff4b4b;"></i>
                        <h5>Bắt đầu tính toán </h5>
                        </body>
                                            
                        
                        """, unsafe_allow_html=True)
                image3 = Image.open("image/im3.png")
                st.image(image3)
                
            with col2:
                st.markdown("""
                        <head>
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                        </head>
                        <body>

                        <i class="fa-solid fa-2 fa-beat" style="font-size:70px;color: #ff4b4b;"></i>
                        <h5>Chọn chức năng mong muốn</h5>
                        </body>
                                            
                        
                        """, unsafe_allow_html=True)
                image2 = Image.open("image/im2.png")
                st.image(image2)
                st.markdown(
                """
                <style>
                .b {
                    margin-top: 50px ;
                    }
                </style>

                <div class="b"></div>
                """,
                unsafe_allow_html=True
            )
                st.markdown("""
                        <head>
                        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
                        </head>
                        <body>

                        <i class="fa-solid fa-4 fa-beat" style="font-size:70px;color: #ff4b4b;"></i>
                        <h5>Tải xuống và tiếp tục công việc</h5>
                        </body>
                                            
                        
                        """, unsafe_allow_html=True)
                image4 = Image.open("image/im4.png")
                st.image(image4)
            container.markdown("---")
            footer()
            
    
if __name__ == "__main__":
    main()
    

    

    

