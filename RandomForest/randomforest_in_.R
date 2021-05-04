# To Do! 도시(워싱턴 주 시애틀)의 내일 최고 기온(actual)예측.

# 1. load data
# 
# 2. glimpse, head(), View()
# 
# 3. NA 처리
# 
# 4. factor 형 변환, 변수 전처리
# 
# 5. EDA (산점도, histogram, density)
# 
# 6. 목적변수와 높은 correlation 변수 찾기, 시각화
# 
# 7. train, test 나누기
# 
# 8. 모형생성과 평가
# 
# 9. 모형비교 및 선택
##------------------------------------------------------------------------

rm(list = ls())

library(tidyverse)

features <- read.csv('C:/Users/82102/Downloads/회사자료/report/temps.csv', fileEncoding = 'euc-kr', stringsAsFactors = F, strip.white = T)


# 데이터 파악

head(features)
dim(features)
str(features)
glimpse(features)
summary(features)

# 컬럼 설명
# temp_2 : 2 일 전 최대 기온
# temp_1 : 1 일 전 최대 기온
# average : 과거 평균 최대 기온
# actual : 실제 최대 기온
# friend : 친구의 예측(average +- 20 의 랜덤 값)

##------------------------------------------------------------------------
library(lubridate)

features %>% 
  mutate(date=ymd(paste(year, month, day, sep = '-'))) %>% 
  select(temp_2, temp_1, actual, friend, date) %>% 
  pivot_longer(-c(date)) %>% 
  ggplot(aes(x=date, y=value)) +
  geom_line(aes(color=name)) +
  facet_wrap(~name) +
  theme(legend.position='none')

##------------------------------------------------------------------------
# 원-핫 인코딩(week열)

library(mltools)
library(data.table)

features$week <- as.factor(features$week)
features <- as.data.frame(one_hot(as.data.table(features)))

dim(features) 
head(features)

##------------------------------------------------------------------------
# train/test 나누기

set.seed(42) 

# 1안
features <- features %>% rowid_to_column() 
train <- features %>% sample_frac(0.75)
test <- anti_join(features, train, by='rowid')

nrow(features) == nrow(train) + nrow(test)


# 2안 多 ★★★★★
library(caret)

train_ind <- createDataPartition(features$actual, p=0.75)$Resample1 
train2 <- features[train_ind, ]
test2 <- features[-train_ind, ]


# 데이터가 균등하게 분할 되었는지 시각화

p1 <- features %>% 
  ggplot(aes(x=actual)) +
  geom_histogram() 

p2 <- train2 %>% 
  ggplot(aes(x=actual)) +
  geom_histogram() 

p3 <- test2 %>% 
  ggplot(aes(x=actual)) +
  geom_histogram() 

library(gridExtra)
grid.arrange(p1, p2, p3, nrow=3)


##------------------------------------------------------------------------
test_labels <- test %>% select(actual)

baseline_preds <- test %>% select(average)
baseline_preds

baseline_errors <- abs(baseline_preds - test_labels)

baseline_errors %>% 
  summarise(mean=round(mean(average), 2)) # 4.62

##------------------------------------------------------------------------
library(randomForest)

set.seed(42) 

rf <- randomForest(actual~., data=train2, ntree=200, importance=T)

varImpPlot(rf, type=1, pch=19, col=1, cex=1, main='')

predictions <- predict(rf, newdata = test2)


# 절대 오차 계산
errors <- abs(predictions - test2$actual)

# 평균 절대 오차(mae)
round(mean(errors), 2) # 3.74

# mean absolute percentage error(MAPE)
mape <- 100 * (errors / test2$actual)


accuracy <- 100 - mean(mape)
round(accuracy, 2) # 94.02

##------------------------------------------------------------------------
library(party)

tree <- ctree(actual ~ ., data=train2)
plot(tree)

##------------------------------------------------------------------------
# 가장 중요한 두 가지 변수(temp_1, average)만 있는 새로운 random forest모델

train_important <- train2 %>% select(temp_1, average, actual)
test_important <- test2 %>% select(temp_1, average, actual)

set.seed(42) 

rf_most_important <- randomForest(actual~., data=train_important, ntree=200, importance=T)

predictions <- predict(rf_most_important, newdata = test_important)

# 절대 오차 계산
errors <- abs(predictions - test_important$actual)

# 평균 절대 오차(mae)
round(mean(errors), 2) # 3.52

# mean absolute percentage error(MAPE)
mape <- 100 * (errors / test_important$actual)

accuracy <- 100 - mean(mape)
round(accuracy, 2) # 94.29

##------------------------------------------------------------------------
# 시각화

# 1.
ls(rf)
class(rf$importance)
rf$importance

importance <- rf$importance[, 2] %>% as.data.frame() 

importance %>% 
  rename(value='.') %>% 
  mutate(name=rownames(.)) %>% 
  ggplot(aes(reorder(x=name, -value), y=value, fill=name)) +
  geom_bar(stat='identity') +
  theme(legend.position = 'none', axis.text.x = element_text(angle=90)) +
  labs(x='variable', y='importance')

# 2.
library(scales)

pred1 <- predict(rf, test2)

data.result <- cbind(test2, pred1)  
head(data.result)

data.result %>% 
  mutate(date=ymd(paste(year, month, day, sep = '-'))) %>% 
  select(date, actual, pred1) %>% 
  ggplot(aes(x=date)) +
  geom_point(aes(y=pred1), color='red') +
  geom_line(aes(y=actual), colour='blue') +
  scale_x_date(breaks = date_breaks("1 month"), labels = date_format("%m/%y")) +
  labs(title='Actual and Predicted Values', y='value')
  
# 3.
data.result %>% 
  mutate(date=ymd(paste(year, month, day, sep = '-'))) %>% 
  select(date, actual, temp_1, average, friend) %>% 
  pivot_longer(-c(date)) %>% 
  ggplot(aes(x=date, y=value)) +
  geom_line(aes(color=name), size=1.0)