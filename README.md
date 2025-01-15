# Student-Performance-Data-Student-Alcohol-Consumption
1. Student Performance Data & Student Alcohol Consumption, data available on kaggle.com is used for prediction. I merged both files to find the percentage of failures with respect to alcohol consumption. New data named as Student_data.

2. In the data exploration dimension, 395 observations with 33 columns are found. Some are categorical and some are integer variables. 48.48% are Integer variables and 51.52% are categorical variables.Some visualizations are done on the data. We found that student consume more alcohol in weekends.The very high alcohol 
 consumption category has an interesting shape as it expands while others tend to decrease. We can also notice it is nicely shaped as a bottle. Interestingly student age with 16 years is highest in all areas like less alcohol to high consumption. But most of the 16 years students live with their mother. And Femal students are getting more support from their family then males. And same with school also. But surprisingly schools are not supporting students more.

3. Removing all the N/A in the data set (student_data), and removing all the non-useful variables. Using Mother education & Father Education, I developed Well 
 ducated family. Because Father & mother are belonging to one family. We can observe that students with high failure rate are belongs to less educated families & less educated families and surprisingly students belongs to high educated families has not failed in exams.

4. Updating the col of well_educated_family in the Student_data_new for dummy data frame student_data_new_1. Creating a dummy for a well_educated_family(using father education & mother education) with family_education. And Create dummy of Gender, 1 => Male 0 => Female. Applying “heatmaply” doing visualization for raw data( student_data) and applying visualization on normalized data.
   
5. PCA is one of the most used unsupervised learning algorithms, Doing PCA on the data set, and using “biplot” a two-dimensional chart that represents the relationship between the rows and columns of a data set. And doing MDS projection. 

6. Doing Random forest and SVM to the data set, I got accuracy around 74% for randomforest & around 62% for SVM. Using “rpart” for building classification and regression trees.

7. At last ROC of best Randomforest model is plotted and Area under the curve is calculated ,which is 78.98%. ROC is better performance metrics as compared to Accuracy if data is imbalanced.
