# -*- coding: utf-8 -*-
"""loan_approval.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15O8SIX4hfNrtG3KJlI8ALty4AXyi_iG0
"""

# unzip data and delete zip
#!unzip /content/HomeBuyerDat.zip > /dev/null
#!rm /content/HomeBuyerDat.zip > /dev/null

import pandas as pd
home_buyer_df = pd.read_csv("HomeBuyerDat.csv")
home_buyer_df.head(5)

#score from 0-1 where 0 is a rejection and 1 is an approval
def calc_score(id, df):
  """
  Given a user ID, calculate the score that determines their approval or rejection.
  Input:
    id - int
    df - pandas dataframe
  Output:
    score - int from 0 to 1
  """

def calc_LTV(id, df):
  """
  Given a user ID, calculate their LTV.
  Input:
    id - int
    df - pandas dataframe
  Output:
    ltv - calculated ltv in decimal form
    pmi - pmi in decimal form if necessary, else 0.0
  """
  house_value = df.loc[id-1]['AppraisedValue']
  down_payment = df.loc[id-1]['DownPayment']

  ltv_decimal = ((house_value - down_payment) / house_value)
  pmi_decimal = .01 if ltv_decimal >= .8 else 0.0

  return ltv_decimal, pmi_decimal

#example
ltv_dec, pmi_dec = calc_LTV(3, home_buyer_df)
ltv_dec, pmi_dec

def calc_DTI(id, pmi, df):
  """
  Given a user ID and PMI, calculate their DTI.
  Input:
    id - int
    pmi - float (decimal form)
    df - pandas dataframe
  Output:
    dti
  """
  individual = df.loc[id-1]
  mortgage = individual['MonthlyMortgagePayment']
  mortgage += (pmi * individual['AppraisedValue']) / 12
  expenses = individual['CreditCardPayment'] + individual['CarPayment'] + individual['StudentLoanPayments'] + mortgage

  return expenses / individual['GrossMonthlyIncome']

dti_dec = calc_DTI(3, pmi_dec, home_buyer_df)
dti_dec

def approve_func(id, df):
  """
  Given a user ID and corresponding LTV and DTI, approve or deny their loan.
  Input:
    id - int
    df - pandas df
  Output:
    score - int where 0 is a rejection and 1 is an approval
    reasons - list of strings with reason labels
  """
  reasons = []
  ltv, pmi = calc_LTV(id, df)
  dti = calc_DTI(id, pmi, df)

  if df.loc[id-1]['CreditScore'] < 640:
    reasons.append("creditscore")
    return 0, reasons

  score = .5

  #if ltv in range 80-100, 20 possible values to scale up from .5 to 1
  if ltv >= .80:
   score -= (((ltv - .80)*100/20) ** 2)/100
   reasons.append("ltv")
  else:
    score += .25

  #if dti is over 43
  if dti > .43:
    score -= (((dti - .43)*100/57) ** 2)/100
    reasons.append("dti")
  else:
      score += .25

  print("LTV: " + str(ltv * 100) + "%")
  print("DTI: " + str(dti * 100) + "%")
  return 0 if score < .5 else 1, reasons

#example
approve_func(12, home_buyer_df)
