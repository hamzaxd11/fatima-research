"""
Analyze the SPSS columns to map them to knowledge and practice questions.
"""

from src.data_loader import load_spss_file

# Load the SPSS file
df, metadata = load_spss_file('menstrual hygiene spss.sav fatima and ayesha (1).sav')

print("=" * 80)
print("ALL COLUMNS IN ORDER")
print("=" * 80)

for i, col in enumerate(df.columns, 1):
    print(f"{i:2d}. {col}")

print("\n" + "=" * 80)
print("POTENTIAL KNOWLEDGE QUESTIONS (Section III)")
print("=" * 80)
print("Based on the requirements, these should be questions about menstrual knowledge:")
print()

knowledge_candidates = [
    'RangeOfUsualAgeOfMenarche',  # Q15
    'WhatDoYouThinkAboutThePrecessofMensturation',  # Q16
    'OrganOfBodyResponsibleForMenarche',  # Q17
    'RangeOfNormalDurationOfMensturalBleeding',  # Q18
    'AfterHowManyDaysDoYouMensturateEveryMonth',  # Q19
    'WhichTypeOfAbsorbsentToBeUsedDuringMensturation',  # Q20
    'HowManyTimePerDayClothandSanitaryPadTOBeChanged',  # Q22
    'HowTheClothAndSanitaryPadToBeDisposeOF',  # Q23
    'WhereTheSanitaryPadToBeDispoadOF',  # Q24
]

for i, col in enumerate(knowledge_candidates, 1):
    if col in df.columns:
        print(f"  {i}. {col}")
        # Show value distribution
        print(f"     Values: {sorted(df[col].dropna().unique())}")
    else:
        print(f"  {i}. {col} - NOT FOUND")

print("\n" + "=" * 80)
print("POTENTIAL PRACTICE QUESTIONS (Section IV)")
print("=" * 80)
print("Based on the requirements, these should be questions about actual practices:")
print()

practice_candidates = [
    'WhichTypeOfAbsorbentDoYouUseDuringMensturation',  # Q25
    'IfUseClothDoYouRegularyWashClothPadWithSoapAndWater',  # Q26
    'DoYouDryTheClothINSun',  # Q27
    'HowManyTimeUsualyChangeTheClothandSanitaryPad',  # Q30
    'UsePaperToDisposeThePadByWrapping',  # Q31
    'WhereDisposeTheUsedPads',  # Q32
    'HowManyTimesTakeBathDuringMensturation',  # Q33
    'CleanYourExternalGenitaliaThroughlyWaterDuringMensturation',  # Q34
    'AfterThatWashHandsWithSoapAndWater',  # Q35
]

for i, col in enumerate(practice_candidates, 1):
    if col in df.columns:
        print(f"  {i}. {col}")
        # Show value distribution
        print(f"     Values: {sorted(df[col].dropna().unique())}")
    else:
        print(f"  {i}. {col} - NOT FOUND")

print("\n" + "=" * 80)
print("RECOMMENDATIONS")
print("=" * 80)
print("We need to:")
print("1. Map the actual column names to knowledge/practice questions")
print("2. Understand the scoring rules for each question")
print("3. Update the data processor to use the correct column names")
