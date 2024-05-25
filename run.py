import os
import src.pandas_frame
import src.ivcurve
import src.transmission
import src.ref_transmission
#import src.flat_transmission
import matplotlib.pyplot as plt

def main():
    # CSV 파일을 저장할 디렉토리 경로
    csv_directory = os.path.join('res', 'CSV')
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)

    final_df = src.pandas_frame.pandas_data()
    print(final_df)
    csv_file_path = os.path.join(csv_directory, 'pandas.csv')  # res/CSV 디렉토리에 있는 pandas.csv 파일 경로
    final_df.to_csv(csv_file_path, index=False)


    # JPG 파일 저장 디렉토리 생성
    jpgs_directory = os.path.join('res', 'jpgs')
    if not os.path.exists(jpgs_directory):
        os.makedirs(jpgs_directory)




def plot_and_save_all_graphs(jpgs_directory):
    # 그래프를 그리기 위한 subplot 생성
    plt.figure(figsize=(15, 10))

    # 첫 번째 서브플롯에 IV curve 그리기
    plt.subplot(2, 2, 1)
    src.ivcurve.plot_and_save_graphs(jpgs_directory)

    # 두 번째 서브플롯에 transmission 그래프 그리기
    plt.subplot(2, 2, 2)
    src.transmission.plot_and_save_graphs(jpgs_directory)

    # 세 번째 서브플롯에 ref transmission 그래프 그리기
    plt.subplot(2, 2, 3)
    src.ref_transmission.plot_and_save_graphs(jpgs_directory)

    # 네 번째 서브플롯에 flat transmission 그래프 그리기 (모듈이 없을 시 주석 처리)
    # plt.subplot(2, 2, 4)
    # src.flat_transmission.plot_and_save_graphs(jpgs_directory)

    plt.subplots_adjust(wspace=0.5)  # 좌우 간격 조정
    plt.subplots_adjust(hspace=0.3)  # 위아래 간격 조정

 # 그래프 생성 및 저장
    plot_and_save_all_graphs(jpgs_directory)

if __name__ == "__main__":
    main()