#-*- coding: utf-8 -*-
# correlation analysis(상관분석)
from math import sqrt
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
# font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
# rc('font', family=font_name)

def hi():
    print('hi')



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


