##Project Title: Coffee Shop Sales Analysis
Introduction

In this project, I worked with a coffee shop sales dataset to understand how sales vary across different stores, products, and time periods. The dataset includes details such as transaction dates, store locations, product categories, product types, quantity sold, and total sales amount.

The main goal of this project was to explore the data carefully, find meaningful patterns, and understand what actually drives sales in a coffee shop. Through this project, I focused on learning how to analyze real business data and convert numbers into useful insights.

What I did in this project (Step-by-Step)
1. Data Cleaning and Initial Preparation

I started by loading the dataset and doing some basic checks to understand the structure of the data. I verified column names, data types, and overall data quality.

The transaction_date column was converted into datetime format so that time-based analysis could be done properly. From this column, I also created a new month feature, which helped in analyzing monthly sales trends.

The dataset was already cleaned, so no major missing value handling was required. After these steps, the data was ready for further analysis.

2. Exploring the Data

Next, I explored the categorical columns in the dataset such as:

Store location

Product category

Product type

Weekday

Month

I checked unique values and value counts to understand how many stores and product types were present and how transactions were distributed across days and months. This step helped me become familiar with the dataset and made the later analysis easier to interpret.

3. Store Location Analysis

After understanding the data, I analyzed sales based on store location. I grouped the data by store location and calculated total sales for each store.

From this analysis, it was clear that some store locations perform much better than others. This difference could be due to factors like customer traffic, location demand, or store size. This showed that store location plays an important role in overall sales performance.

4. Product Category and Product Type Analysis

Then I focused on product-level analysis. I grouped the data by product category to see which categories contribute the most to total revenue.

I also analyzed product types by looking at the total quantity sold. This helped me identify the best-selling products as well as products that sell less frequently. From this part of the analysis, it became clear that a small number of products contribute a large portion of total sales.

5. Sales Analysis by Time (Weekday and Month)

Time-based analysis gave some very interesting insights. I analyzed average sales across different weekdays to understand customer buying patterns during the week.

Some weekdays showed higher average sales, indicating peak business days, while others were comparatively slower. I also looked at monthly sales trends and observed variations in sales across different months, suggesting possible seasonal effects.

6. Pivot Table Analysis

To analyze multiple factors together, I created pivot tables such as:

Product category vs store location vs total sales

Weekday vs store location vs total sales

Product type vs product category vs quantity sold

Month vs product category vs quantity sold

These pivot tables made it easier to compare performance across different combinations and helped in gaining deeper insights.

7. Interactive Dashboard

Finally, I built an interactive dashboard using Streamlit. The dashboard allows users to filter data by store location, product category, and month.

Based on the selected filters, the dashboard dynamically shows key metrics like total revenue, total transactions, quantity sold, and average bill value. Visualizations such as sales trends and top-selling products make the insights easier to understand and more engaging.

Final Conclusion (What I Learned)

By working on this project, I learned that coffee shop sales are influenced by several factors, but the most important ones are:

Store location

Product category and product type

Time factors such as weekday and month

Popular products and busy days contribute heavily to overall revenue, while location plays a major role in determining store performance.

Overall, this project helped me improve my data analysis skills, especially in exploratory data analysis, grouping, pivot tables, and building interactive dashboards. More importantly, it taught me how to think from a business point of view and turn raw data into meaningful insights.

If you want, I can:

Make it shorter and crisper

Rewrite it in first-year student style

Convert it into resume-ready bullet points

Just tell me 👍
