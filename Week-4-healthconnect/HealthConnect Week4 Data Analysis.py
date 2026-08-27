import pandas as pd
df =pd.read_csv("g:\My Drive\Books\Week 4\HealthConnect Appointment Data Cleaned.csv")
df.head()

print(df.shape)
print(df.columns.tolist())

df.isnull().sum()

print(df['appointment_id'].duplicated().sum())
print(df.duplicated().sum())

no_show_rate = (df['appointment_outcome'] == 'No-Show').mean() * 100
print(f"Overall no-show rate: {no_show_rate:.1f}%")

bins = [-1, 0, 7, 999]
labels = ['Same-day', '1-7 days', '8+ days']
df['lead_band'] = pd.cut(df['booking_lead_days'], bins=bins, labels=labels)

print(df.groupby('lead_band', observed=True)['appointment_outcome'].apply(lambda s: (s == 'No-Show').mean() * 100))

