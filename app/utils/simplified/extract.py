import re


def extract_salary_range(salarylabel: str ):
        normalized_salary = {
            'min_salary': None,
            'max_salary': None,
            'currency': None,
            'period': None,
            'has_salary_info': False
        }
        if salarylabel is None:
            return normalized_salary
        
        try:
            # แยกส่วนของตัวเลข
            numbers = re.findall(r'[\d,]+', salarylabel)
            if len(numbers) > 0:  # มีตัวเลขอย่างน้อย 1 ตัว
                normalized_salary['has_salary_info'] = True
                if len(numbers) >= 2:  # กรณีเป็นช่วง
                    normalized_salary['min_salary'] = float(numbers[0].replace(',', ''))
                    normalized_salary['max_salary'] = float(numbers[1].replace(',', ''))
                else:  # กรณีมีเลขเดียว
                    single_salary = float(numbers[0].replace(',', ''))
                    normalized_salary['min_salary'] = single_salary
                    normalized_salary['max_salary'] = single_salary

                # กำหนดสกุลเงิน
                if any(currency in salarylabel for currency in ['฿', 'THB', 'บาท']):
                    normalized_salary['currency'] = 'THB'
                elif any(currency in salarylabel for currency in ['$', 'USD']):
                    normalized_salary['currency'] = 'USD'

                # กำหนดช่วงเวลา
                if any(period in salarylabel.lower() for period in ['per month', 'monthly', 'เดือน']):
                    normalized_salary['period'] = 'monthly'
                elif any(period in salarylabel.lower() for period in ['per hour', 'hourly', 'ชั่วโมง']):
                    normalized_salary['period'] = 'hourly'
                elif any(period in salarylabel.lower() for period in ['per year', 'yearly', 'annual', 'ปี']):
                    normalized_salary['period'] = 'yearly'
                
        except Exception as e:
            print(f"Error processing salary: {salarylabel}, Error: {str(e)}")
            return {
                'min_salary': None,
                'max_salary': None,
                'currency': None,
                'period': None,
                'has_salary_info': False
            }
                
        return normalized_salary