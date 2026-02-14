"""
Data Processing Module

This module provides functions for calculating derived fields and scores
from the menstrual hygiene survey data.
"""

import pandas as pd
import numpy as np
from typing import List, Optional
import warnings


def calculate_per_capita_income(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate per capita income for each record.
    
    Per capita income = Income Per Month / Total Family Members
    
    Handles missing values and division by zero according to requirements:
    - If income or family members are missing/null, per capita income is null
    - If family members is zero, per capita income is null (prevents division by zero)
    - Result is rounded to 2 decimal places
    
    Args:
        df: DataFrame with 'income_per_month' and family member columns
        
    Returns:
        DataFrame with added 'per_capita_income' column
        
    Requirements: 2.1, 2.2, 2.3, 2.5
    """
    df = df.copy()
    
    # Calculate total family members if not already present
    if 'total_family_members' not in df.columns:
        # Try different column name variations
        male_col = None
        female_col = None
        
        # Check for column name variations
        for col in df.columns:
            col_lower = col.lower()
            if 'male' in col_lower and 'family' in col_lower and 'female' not in col_lower:
                male_col = col
            elif 'female' in col_lower and 'family' in col_lower:
                female_col = col
        
        # Handle missing values in family member counts
        if male_col and male_col in df.columns:
            male_members = pd.to_numeric(df[male_col], errors='coerce').fillna(0)
        else:
            male_members = pd.Series([0] * len(df))
        
        if female_col and female_col in df.columns:
            female_members = pd.to_numeric(df[female_col], errors='coerce').fillna(0)
        else:
            female_members = pd.Series([0] * len(df))
        
        df['total_family_members'] = male_members + female_members
    
    # Initialize per_capita_income column with NaN
    df['per_capita_income'] = np.nan
    
    # Get income column - try different name variations
    income_col = None
    for col in df.columns:
        if 'income' in col.lower() and 'capita' not in col.lower():
            income_col = col
            break
    
    if income_col and income_col in df.columns:
        income = pd.to_numeric(df[income_col], errors='coerce')
    else:
        income = pd.Series([np.nan] * len(df))
        
    # Drop "IncomePerCapita" if it exists (but isn't the calculated one yet) to identify confusion
    # The new calculated column is "per_capita_income"
    # If there is a completely empty "IncomePerCapita" column from SPSS, it causes data quality false alarms
    for col in df.columns:
        if col.lower().replace("_", "") == "incomepercapita" and col != "income_per_month":
            # Check if it's mostly empty
            if df[col].isna().sum() > len(df) * 0.9:
                # Drop it to avoid noise
                df.drop(columns=[col], inplace=True)
                warnings.warn(f"Dropped empty '{col}' column to prefer calculated 'per_capita_income'")
    
    family_size = pd.to_numeric(df['total_family_members'], errors='coerce')
    
    # Calculate per capita income only for valid records
    # Valid record criteria:
    # 1. Income is not null/missing
    # 2. Family size is not null/missing
    # 3. Family size is greater than 0 (prevents division by zero)
    # 4. Income is non-negative (negative income doesn't make sense)
    #
    # Per capita income formula: Total Monthly Income / Total Family Members
    # This provides a measure of economic resources available per person
    # Useful for comparing economic status across families of different sizes
    valid_mask = (income.notna()) & (family_size.notna()) & (family_size > 0) & (income >= 0)
    
    if valid_mask.any():
        # Calculate and round to 2 decimal places for currency precision
        df.loc[valid_mask, 'per_capita_income'] = (income[valid_mask] / family_size[valid_mask]).round(2)
    
    # Log warnings for problematic records to help with data quality assessment
    # These warnings inform the user about data issues without stopping the analysis
    
    # Case 1: Division by zero prevention
    # When family size is 0, we cannot calculate per capita income
    # This is set to null rather than causing a runtime error
    zero_family = (family_size == 0) & income.notna()
    if zero_family.any():
        warnings.warn(f"Division by zero prevented for {zero_family.sum()} records with zero family members")
    
    # Case 2: Missing data handling
    # When either income or family size is missing, per capita income cannot be calculated
    # These records are excluded from per capita income analysis but retained in dataset
    missing_data = (income.isna() | family_size.isna()) & ~zero_family
    if missing_data.any():
        warnings.warn(f"Per capita income set to null for {missing_data.sum()} records with missing income or family size")
    
    return df


def calculate_knowledge_score(df: pd.DataFrame, question_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calculate knowledge score based on Section III questionnaire responses.
    
    Knowledge score ranges from 0 to 9 based on correct responses to 9 questions.
    Missing responses are assigned a score of 0.
    
    Scoring rules from questionnaire:
    Q1 (RangeOfUsualAgeOfMenarche): 2=1 point, else 0
    Q2 (WhatDoYouThinkAboutThePrecessofMensturation): 2=1 point, else 0  
    Q3 (OrganOfBodyResponsibleForMenarche): 3=1 point, else 0
    Q4 (RangeOfNormalDurationOfMensturalBleeding): 4=1 point, else 0
    Q5 (AfterHowManyDaysDoYouMensturateEveryMonth): 3=1 point, else 0
    Q6 (WhichTypeOfAbsorbsentToBeUsedDuringMensturation): 1-5=1 point each
    Q7 (HowManyTimePerDayClothandSanitaryPadTOBeChanged): 1-4=1 point each
    Q8 (HowTheClothAndSanitaryPadToBeDisposeOF): 1=1 point, 2=0
    Q9 (WhereTheSanitaryPadToBeDispoadOF): 2=1 point, else 0
    
    Args:
        df: DataFrame with Section III question columns
        question_columns: List of column names for Section III questions.
                         If None, uses actual SPSS column names
        
    Returns:
        DataFrame with added 'knowledge_score' column
        
    Requirements: 3.1, 3.2, 3.3, 3.4
    """
    df = df.copy()
    
    # Default question columns mapping to actual SPSS columns
    if question_columns is None:
        question_columns = [
            'RangeOfUsualAgeOfMenarche',
            'WhatDoYouThinkAboutThePrecessofMensturation',
            'OrganOfBodyResponsibleForMenarche',
            'RangeOfNormalDurationOfMensturalBleeding',
            'AfterHowManyDaysDoYouMensturateEveryMonth',
            'WhichTypeOfAbsorbsentToBeUsedDuringMensturation',
            'HowManyTimePerDayClothandSanitaryPadTOBeChanged',
            'HowTheClothAndSanitaryPadToBeDisposeOF',
            'WhereTheSanitaryPadToBeDispoadOF'
        ]
    
    # Filter to only existing columns
    existing_columns = [col for col in question_columns if col in df.columns]
    
    if not existing_columns:
        warnings.warn("No knowledge question columns found in dataset")
        df['knowledge_score'] = 0
        return df
    
    # Initialize score column
    df['knowledge_score'] = 0
    
    # Scoring rules for each question based on questionnaire guidelines
    # Each question has specific correct answers that earn 1 point
    # Missing or incorrect responses earn 0 points
    scoring_rules = {
        # Q1: What is the usual age range for menarche?
        # Correct answer: 10-14 years (coded as 2.0)
        'RangeOfUsualAgeOfMenarche': {2.0: 1},
        
        # Q2: What do you think about the process of menstruation?
        # Correct answer: Physiological/Normal process (coded as 2.0)
        'WhatDoYouThinkAboutThePrecessofMensturation': {2.0: 1},
        
        # Q3: Which organ of the body is responsible for menarche?
        # Correct answer: Uterus (coded as 3.0)
        'OrganOfBodyResponsibleForMenarche': {3.0: 1},
        
        # Q4: What is the normal duration range of menstrual bleeding?
        # Correct answer: 3-7 days (coded as 4.0)
        'RangeOfNormalDurationOfMensturalBleeding': {4.0: 1},
        
        # Q5: After how many days do you menstruate every month?
        # Correct answer: 28 days (coded as 3.0)
        'AfterHowManyDaysDoYouMensturateEveryMonth': {3.0: 1},
        
        # Q6: Which type of absorbent should be used during menstruation?
        # Any valid option earns 1 point (awareness of options)
        # Options: 1=Cloth, 2=Cotton, 3=Sanitary pad, 4=Tampon, 5=Other
        'WhichTypeOfAbsorbsentToBeUsedDuringMensturation': {1.0: 1, 2.0: 1, 3.0: 1, 4.0: 1, 5.0: 1},
        
        # Q7: How many times per day should cloth/pad be changed?
        # Any valid option earns 1 point (awareness of need to change)
        # Options: 1=Once, 2=Twice, 3=Thrice, 4=More than thrice
        'HowManyTimePerDayClothandSanitaryPadTOBeChanged': {1.0: 1, 2.0: 1, 3.0: 1, 4.0: 1},
        
        # Q8: How should cloth/pad be disposed?
        # Correct answer: Wrapped in paper (coded as 1.0)
        'HowTheClothAndSanitaryPadToBeDisposeOF': {1.0: 1},
        
        # Q9: Where should sanitary pad be disposed?
        # Correct answer: In dustbin (coded as 2.0)
        'WhereTheSanitaryPadToBeDispoadOF': {2.0: 1}
    }
    
    # Calculate score based on scoring rules
    # For each question, check if the response matches any correct answer
    # and add the corresponding points to the total score
    for col in existing_columns:
        if col in scoring_rules:
            # Convert to numeric, coerce errors to NaN
            # This handles any non-numeric values gracefully
            responses = pd.to_numeric(df[col], errors='coerce')
            
            # Apply scoring rule for this question
            # For each correct answer value, find matching responses and add points
            for value, points in scoring_rules[col].items():
                df.loc[responses == value, 'knowledge_score'] += points
    
    # Ensure score is integer type
    df['knowledge_score'] = df['knowledge_score'].astype(int)
    
    # Validate score range (0-9)
    invalid_scores = (df['knowledge_score'] < 0) | (df['knowledge_score'] > 9)
    if invalid_scores.any():
        warnings.warn(f"Invalid knowledge scores detected for {invalid_scores.sum()} records. Clamping to valid range.")
        df.loc[df['knowledge_score'] < 0, 'knowledge_score'] = 0
        df.loc[df['knowledge_score'] > 9, 'knowledge_score'] = 9
    
    return df


def calculate_practice_score(df: pd.DataFrame, question_columns: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Calculate practice score based on Section IV questionnaire responses.
    
    Practice score ranges from 0 to 7 based on responses to 7 questions.
    Missing responses are assigned a score of 0.
    
    Scoring rules from questionnaire:
    Q1 (WhichTypeOfAbsorbentDoYouUseDuringMensturation): 1-5=1 point each
    Q2 (UsePaperToDisposeThePadByWrapping): 1=1 point, 2=0
    Q3 (WhereDisposeTheUsedPads): 1=1 point, else 0
    Q4 (HowManyTimeUsualyChangeTheClothandSanitaryPad): 1-4=1 point each
    Q5 (HowManyTimesTakeBathDuringMensturation): 1=1 point, else 0
    Q6 (CleanYourExternalGenitaliaThroughlyWaterDuringMensturation): 1=1 point, 2=0
    Q7 (AfterThatWashHandsWithSoapAndWater): 1=1 point, else 0
    
    Args:
        df: DataFrame with Section IV question columns
        question_columns: List of column names for Section IV questions.
                         If None, uses actual SPSS column names
        
    Returns:
        DataFrame with added 'practice_score' column
        
    Requirements: 4.1, 4.2, 4.3, 4.4
    """
    df = df.copy()
    
    # Default question columns mapping to actual SPSS columns
    if question_columns is None:
        question_columns = [
            'WhichTypeOfAbsorbentDoYouUseDuringMensturation',
            'UsePaperToDisposeThePadByWrapping',
            'WhereDisposeTheUsedPads',
            'HowManyTimeUsualyChangeTheClothandSanitaryPad',
            'HowManyTimesTakeBathDuringMensturation',
            'CleanYourExternalGenitaliaThroughlyWaterDuringMensturation',
            'AfterThatWashHandsWithSoapAndWater'
        ]
    
    # Filter to only existing columns
    existing_columns = [col for col in question_columns if col in df.columns]
    
    if not existing_columns:
        warnings.warn("No practice question columns found in dataset")
        df['practice_score'] = 0
        return df
    
    # Initialize score column
    df['practice_score'] = 0
    
    # Scoring rules for each question based on questionnaire guidelines
    # Each question has specific correct/appropriate answers that earn 1 point
    # Missing or inappropriate responses earn 0 points
    scoring_rules = {
        # Q1: Which type of absorbent do you use during menstruation?
        # Any valid option earns 1 point (indicates use of proper absorbent)
        # Options: 1=Cloth, 2=Cotton, 3=Sanitary pad, 4=Tampon, 5=Other
        'WhichTypeOfAbsorbentDoYouUseDuringMensturation': {1.0: 1, 2.0: 1, 3.0: 1, 4.0: 1, 5.0: 1},
        
        # Q2: Do you use paper to dispose the pad by wrapping?
        # Correct answer: Yes (coded as 1.0) - proper hygiene practice
        'UsePaperToDisposeThePadByWrapping': {1.0: 1},
        
        # Q3: Where do you dispose the used pads?
        # Correct answer: In dustbin (coded as 1.0) - proper disposal
        'WhereDisposeTheUsedPads': {1.0: 1},
        
        # Q4: How many times do you usually change the cloth/pad?
        # Any valid option earns 1 point (awareness of need to change)
        # Options: 1=Once, 2=Twice, 3=Thrice, 4=More than thrice
        'HowManyTimeUsualyChangeTheClothandSanitaryPad': {1.0: 1, 2.0: 1, 3.0: 1, 4.0: 1},
        
        # Q5: How many times do you take bath during menstruation?
        # Correct answer: Daily (coded as 1.0) - proper hygiene practice
        'HowManyTimesTakeBathDuringMensturation': {1.0: 1},
        
        # Q6: Do you clean your external genitalia thoroughly with water?
        # Correct answer: Yes (coded as 1.0) - proper hygiene practice
        'CleanYourExternalGenitaliaThroughlyWaterDuringMensturation': {1.0: 1},
        
        # Q7: After that, do you wash hands with soap and water?
        # Correct answer: Yes (coded as 1.0) - proper hygiene practice
        'AfterThatWashHandsWithSoapAndWater': {1.0: 1}
    }
    
    # Calculate score based on scoring rules
    for col in existing_columns:
        if col in scoring_rules:
            # Convert to numeric, coerce errors to NaN
            responses = pd.to_numeric(df[col], errors='coerce')
            # Apply scoring rule for this question
            for value, points in scoring_rules[col].items():
                df.loc[responses == value, 'practice_score'] += points
    
    # Ensure score is integer type
    df['practice_score'] = df['practice_score'].astype(int)
    
    # Validate score range (0-7)
    invalid_scores = (df['practice_score'] < 0) | (df['practice_score'] > 7)
    if invalid_scores.any():
        warnings.warn(f"Invalid practice scores detected for {invalid_scores.sum()} records. Clamping to valid range.")
        df.loc[df['practice_score'] < 0, 'practice_score'] = 0
        df.loc[df['practice_score'] > 7, 'practice_score'] = 7
    
    return df


def create_scored_dataset(
    df: pd.DataFrame,
    knowledge_columns: Optional[List[str]] = None,
    practice_columns: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Orchestrate all scoring calculations to create the complete scored dataset.
    
    This function applies all transformations in sequence:
    1. Calculate total family members (if needed)
    2. Calculate per capita income
    3. Calculate knowledge score
    4. Calculate practice score
    5. Calculate total score (knowledge + practice)
    
    The order of operations is important:
    - Per capita income must be calculated first as it creates total_family_members
    - Knowledge and practice scores are independent and can be calculated in any order
    - Total score depends on both knowledge and practice scores
    
    Args:
        df: Original DataFrame from SPSS file
        knowledge_columns: Optional list of Section III question column names
        practice_columns: Optional list of Section IV question column names
        
    Returns:
        DataFrame with all original columns plus derived fields:
        - total_family_members: Sum of male and female family members
        - per_capita_income: Monthly income divided by family size
        - knowledge_score: Score from 0-9 based on Section III responses
        - practice_score: Score from 0-7 based on Section IV responses
        - total_score: Sum of knowledge and practice scores (0-16)
        
    Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 4.1, 4.2, 4.3
    """
    # Start with a copy to avoid modifying original
    scored_df = df.copy()
    
    # Step 1: Calculate per capita income (also calculates total_family_members)
    scored_df = calculate_per_capita_income(scored_df)
    
    # Step 2: Calculate knowledge score
    scored_df = calculate_knowledge_score(scored_df, knowledge_columns)
    
    # Step 3: Calculate practice score
    scored_df = calculate_practice_score(scored_df, practice_columns)
    
    # Step 4: Calculate total score
    scored_df['total_score'] = scored_df['knowledge_score'] + scored_df['practice_score']
    
    return scored_df
