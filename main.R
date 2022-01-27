library(readxl)

print("Initializing")
result_excel <- read_excel("result/result_excel.xlsx")
table <- result_excel
table <- table[order(table$Read), ]
table <- table[table[, "Popularity"] > 0,]
popularities <- table$Popularity
reads <- table$Read
x <- seq(1, length(reads))

print("Generate graphic")
plot(x, reads, col="red", xlab="Music", ylab="Reads")
par(new=TRUE)
plot(x, popularities, col="blue", axes = FALSE, xlab="", ylab="")
axis(side = 4, at = pretty(range(popularities)))      
mtext("Popularity", side = 4, line = 50)

print("Show corelation")
plot(popularities, reads, xlab = "Popularity", ylab = "Read", col="blue")

print("Test corelation from pearson")
pearson_result <- cor.test(popularities, reads)
print(pearson_result)

print("Test corelation from spearman")
print(cor.test(popularities, reads, method="spearman"))


print("Linear model")
linearModel <- lm(reads ~ popularities)
print(linearModel)
abline(linearModel, col="red")


print("Normal's law")
print("Histogram")
hist(reads, xlab="Read")
mean_reads <- mean(reads)
print(mean_reads)
sigma_reads <- sd(reads)
print(sigma_reads)
norm_reads <- dnorm(reads, mean=mean_reads, sd=sigma_reads)
par(new=TRUE)
plot(reads, norm_reads, type="l", col="red", axes = FALSE, xlab="", ylab="")
axis(side = 4, at = pretty(range(norm_reads)))      
mtext("Norm", side = 4)

print("Shapiro-Wilk's test")
shapiro_result <- shapiro.test(reads)
print(shapiro_result)

print("QQ-Plot")
qqplot(norm_reads, reads, col="red", type="l")
