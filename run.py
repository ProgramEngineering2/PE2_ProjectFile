import matplotlib.pyplot as plt
import os
import src.pandas_frame

def main():
    # CSV 파일을 저장할 디렉토리 경로
    csv_directory = os.path.join('res', 'CSV')
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)


    final_df = src.pandas_frame.pandas_data()
    print(final_df)
    csv_file_path = os.path.join(csv_directory, 'pandas.csv')  # res/CSV 디렉토리에 있는 pandas.csv 파일 경로
    final_df.to_csv(csv_file_path, index=False)


if __name__ == "__main__":
    main()
