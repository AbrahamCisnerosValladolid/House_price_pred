# House pricing prediction in Bangalore

[Link to the proyect](https://github.com/AbrahamCisnerosValladolid/House_price_pred/blob/main/main.ipynb)

# House Pricing Prediction with Linear Regression

## Overview  
This project predicts house prices in Bengaluru, India, using **linear regression**. The dataset includes features like location, size, square footage, and amenities. The workflow covers data cleaning, preprocessing, exploratory analysis, and model building.

## Dataset  
`bengaluru_house_prices.csv` contains:  
- `area_type`: Type of area (e.g., Built-up Area, Carpet Area)  
- `availability`: Availability status  
- `location`: Neighborhood  
- `size`: Number of bedrooms (e.g., "2 BHK")  
- `total_sqft`: Total square footage (may include ranges like "1000-1500")  
- `bath`: Number of bathrooms  
- `balcony`: Number of balconies  
- `price`: Target variable (price in INR)  

## Data Cleaning & Preprocessing  
1. **Handling Missing Values**:  
   - Dropped columns with high missing values (`society`, `availability`, `area_type`).  
   - Removed rows with missing values in `size`, `bath`, and `balcony`.  

2. **Feature Engineering**:  
   - Extracted `number_bedrooms` from the `size` column (e.g., "2 BHK" → 2).  
   - Converted `total_sqft` ranges to median values (e.g., "1000-1500" → 1250).  
   - Calculated `price_per_sqft` for outlier detection.  

3. **Outlier Removal**:  
   - Filtered properties with unrealistic square footage (<300 sqft/bedroom).  
   - Applied statistical methods (mean ± standard deviation) to remove price outliers.  

4. **Categorical Data**:  
   - Grouped rare locations into an "other" category.  

## Exploratory Data Analysis (EDA)  
- Visualized distributions of price, square footage, and bedrooms.  
- Analyzed correlations between features and price.  
- Explored location-based price trends.  

## Model Building  
- **Algorithm**: Linear Regression.  
- **Evaluation Metrics**:  
  - Mean Squared Error (MSE)  
  - R-squared (R²)  

## Results  
The model achieved **reasonable accuracy**, with key insights:  
- Location and square footage significantly impact prices.  
- Outlier removal improved model performance.  

## Repository Structure  
