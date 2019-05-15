#-*- coding: utf-8 -*-
# correlation analysis(상관분석)
from math import sqrt
from matplotlib import font_manager, rc #한글이 나오게
import matplotlib.pyplot as plt
# font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
# rc('font', family=font_name)

def hi():
    print('hi')


# plt 그리기
def drawGraph(data, name1, name2):
    plt.figure(figsize=(14, 8))  # plot 크기설정

    # plot 좌표를 위한 list 선언
    li = []
    li2 = []

    for i in critics[name1]:  # i = 키 값
        if i in data[name2]:  # 같은 영화를 평가했을때만
            li.append(critics[name1][i])  # name1의 평점 li[]에 추가
            li2.append(critics[name2][i])  # name2의 평점 li2[]에 추가
            plt.text(critics[name1][i], critics[name2][i], i)  # 영화 제목 text 찍기

    plt.plot(li, li2, 'ro')  # plot그리기

    # 각 축의 크기 설정 (0에서 6까지)
    plt.axis([0, 6, 0, 6])

    # x축과 y축 이름 설정
    plt.xlabel(name1)
    plt.ylabel(name2)

    # 그리기
    plt.show()

# 상관계수 구하기(피어슨상관계수)
def sim_pearson(data, name1, name2):
    sumX = 0  # X의 합
    sumY = 0  # Y의 합
    sumPowX = 0  # X 제곱의 합
    sumPowY = 0  # Y 제곱의 합
    sumXY = 0  # X*Y의 합
    count = 0  # 영화 개수

    for i in data[name1]:  # i = key
        if i in data[name2]:  # 같은 영화를 평가했을때만
            sumX += data[name1][i]
            sumY += data[name2][i]
            sumPowX += pow(data[name1][i], 2)
            sumPowY += pow(data[name2][i], 2)
            sumXY += data[name1][i] * data[name2][i]
            count += 1


    return (sumXY - ((sumX * sumY) / count)) / sqrt(
        (sumPowX - (pow(sumX, 2) / count)) * (sumPowY - (pow(sumY, 2) / count)))

# 전체 인원 상관계수 구하기
def top_match(data, name, index=3, sim_function=sim_pearson):
    li=[]
    for i in data: #딕셔너리를 돌고
        if name!=i: #자기 자신이 아닐때만
            li.append((sim_function(data,name,i),i)) #sim_function()을 통해 상관계수를 구하고 li[]에 추가
    li.sort() #오름차순
    li.reverse() #내림차순
    return li[:index]

# 실제 영화 추천하고 예상 평점 구하기
def getRecommendation(data, person, sim_function=sim_pearson):
    result = top_match(data, person, len(data))

    simSum = 0  # 유사도 합을 위한 변수
    score = 0  # 평점 합을 위한 변수
    li = []  # 리턴을 위한 리스트
    score_dic = {}  # 유사도 총합을 위한 dic
    sim_dic = {}  # 평점 총합을 위한 dic

    for sim, name in result:  # 튜플이므로 한번에
        if sim < 0: continue  # 유사도가 양수인 사람만
        for movie in data[name]:
            if movie not in data[person]:  # name이 평가를 내리지 않은 영화
                score += sim * data[name][movie]  # 그사람의 영화평점 * 유사도
                score_dic.setdefault(movie, 0)  # 기본값 설정
                score_dic[movie] += score  # 합계 구함

                # 조건에 맞는 사람의 유사도의 누적합을 구한다
                sim_dic.setdefault(movie, 0)
                sim_dic[movie] += sim

            score = 0  # 영화가 바뀌었으니 초기화한다

    for key in score_dic:
        score_dic[key] = score_dic[key] / sim_dic[key]  # 평점 총합/ 유사도 총합
        li.append((score_dic[key], key))  # list((tuple))의 리턴을 위해서.
    li.sort()  # 오름차순
    li.reverse()  # 내림차순
    return li


# critics = {
#     '차현석': {
#         '그린 북': 2.5,
#         '어벤져스: 엔드게임': 3.5,
#         '월-E': 3.0,
#         '반지의 제왕: 왕의 귀환': 3.5,
#         '죽은 시인의 사회': 2.5,
#         '지금, 만나러 갑니다': 3.0,
#     },
#     '황해도': {
#         '에이리언 2': 1.0,
#         '메리 포핀스': 4.5,
#         '언터처블: 1%의 우정': 0.5,
#         '그린 북': 1.5,
#         '위대한 쇼맨': 4.5,
#         '어벤져스: 엔드게임': 5.0,
#     },
#     '김미희': {
#         '연평해전': 3.0,
#         '끝까지 간다': 3.5,
#         '그린 북': 1.5,
#         '세 얼간이': 5.0,
#         '명탐정 코난: 순흑의 악몽': 3.0,
#         '어벤져스: 엔드게임': 3.5,
#     },
#     '김준형': {
#         '연평해전': 2.5,
#         '그린 북': 3.0,
#         '명탐정 코난: 순흑의 악몽': 3.5,
#         '어벤져스: 엔드게임': 4.0,
#     },
#     '이은비': {
#         '남한산성': 3.5,
#         '어벤져스: 엔드게임': 3.0,
#         '그린 북': 4.5,
#         '사일런트 힐': 4.0,
#         '아이 캔 스피크': 2.5,
#     },
#     '임명진': {
#         '록키': 3.0,
#         '어벤져스: 엔드게임': 4.0,
#         '그린 북': 2.0,
#         '사일런트 힐': 3.0,
#         '오펀: 천사의 비밀': 3.5,
#         '위대한 쇼맨': 2.0,
#     },
#     '심수정': {
#         '그린 북': 3.0,
#         '어벤져스: 엔드게임': 4.0,
#         '반지의 제왕: 왕의 귀환': 3.0,
#         '여고괴담': 5.0,
#         '지금, 만나러 갑니다': 3.5,
#     },
#     '박병관': {'그린 북': 4.5, '월-E': 1.0,
#              '어벤져스: 엔드게임': 4.0},
# }



# drawGraph(critics, '황해도', '임명진')
# drawGraph(critics, '박병관', '차현석')
# drawGraph(critics,'심수정','차현석')

# print(sim_pearson(critics,'황해도', '임명진'))
# print(sim_pearson(critics,'박병관', '차현석'))
# print(sim_pearson(critics, '심수정', '차현석'))


# print(top_match(critics, '박병관', 6))

# print(getRecommendation(critics, '박병관'))