from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_query = request.form.get('search_query', '').lower()
    sort_order = request.form.get('sort_order', 'desc')

    # Đọc dữ liệu từ file CSV
    try:
        df = pd.read_csv('data/jobs_data.csv')
        print(df.columns)  # In tên các cột
    except Exception as e:
        print(f"Đã xảy ra lỗi khi đọc file CSV: {e}")
        return "Lỗi khi tải dữ liệu công việc."

    # Chuẩn hóa dữ liệu
    df['Job Title'] = df['Job Title'].str.lower()
    df['Company'] = df['Company'].str.lower()

    # Lọc công việc dựa trên truy vấn tìm kiếm
    filtered_jobs = df[(df['Job Title'].str.contains(search_query)) | (df['Company'].str.contains(search_query))]

    # Xử lý sắp xếp, chỉ sắp xếp nếu lương là số
    reverse_order = (sort_order == 'desc')
    
    # Sắp xếp theo mức lương dưới dạng chuỗi
    filtered_jobs_sorted = filtered_jobs.sort_values(by='Salary', ascending=not reverse_order)

    jobs_sorted = filtered_jobs_sorted.rename(columns={'Job Title': 'title', 'Company': 'company', 'Salary': 'salary_str', 'Address': 'address'}).to_dict(orient='records')

    # Xác định nếu không có kết quả
    no_results = len(jobs_sorted) == 0

    return render_template('index.html', jobs=jobs_sorted, search_query=search_query, sort_order=sort_order, no_results=no_results)

if __name__ == '__main__':
    app.run(debug=True)
