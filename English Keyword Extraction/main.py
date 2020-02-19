from datetime import date
def month_to_number(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr':4,
         'may':5,
         'jun':6,
         'jul':7,
         'aug':8,
         'sep':9,
         'oct':10,
         'nov':11,
         'dec':12
        }
    s = string.strip()[:3].lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')


x = date.today()
u_mm = "June"
mm = x.strftime("%B")
_u_mm = month_to_number(u_mm)
_mm = month_to_number(mm)
flag = _u_mm - _mm
print(flag)
print(month_to_number('October'))