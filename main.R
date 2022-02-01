# import package
library(readxl)

# Change working directory
setwd("C:/Users/simon/Project/python3/spotify-stats")

# Load data
print("Initializing")
result_excel <- read_excel("result/result_excel.xlsx") 
table <- result_excel
table <- table[order(table$Read), ] # Sort by reads
table <- table[table[, "Popularity"] > 0,] # filter music with no popularity
popularities <- table$Popularity
reads <- table$Read
x <- seq(1, length(reads)) # List from 1 to length of reads

# Generate first graphic 
print("Generate graphic")
par(mar = c(5,4,4,4) + 0.1)
plot(x, reads, col="red", xlab="Music", ylab="Reads")
par(new=TRUE) # Add a second plot to the same graph
plot(x, popularities, col="blue", axes = FALSE, xlab="", ylab="")
axis(side = 4, at = pretty(range(popularities)))      
mtext("Popularity", side = 4, line = 3)

# Do correlation test
print("Test corelation from pearson")
pearson_result <- cor.test(popularities, reads)
print(pearson_result)
print(pearson_result$estimate^2) # display R^2

print("Test corelation from spearman")
print(cor.test(popularities, reads, method="spearman"))

# Graph of the linear regression
print("Linear model")
plot(popularities, reads, xlab = "Popularity", ylab = "Read", col="blue")
linearModel <- lm(reads ~ popularities)
print(linearModel)
abline(linearModel, col="red")

# Check the normal's law
print("Normal's law")
print("Histogram")
hist(reads, xlab="Read")
mean_reads <- mean(reads) # The average
print(mean_reads)
sigma_reads <- sd(reads) # sigma
print(sigma_reads)
norm_reads <- dnorm(reads, mean=mean_reads, sd=sigma_reads) # build normal's function
par(new=TRUE)
plot(reads, norm_reads, type="l", col="red", axes = FALSE, xlab="", ylab="")
axis(side = 4, at = pretty(range(norm_reads)), ylab="test")      
mtext("Norm", side = 4, line=3)
par(mar = c(5,4,4,4) + 0.1)

# Shapiro-wilk's test
print("Shapiro-Wilk's test")
shapiro_result <- shapiro.test(reads)
print(shapiro_result)

# Show th QQ-plot
print("QQ-Plot")
qqplot(norm_reads, reads, col="red", type="l", xlab="Norm", ylab="Read")
