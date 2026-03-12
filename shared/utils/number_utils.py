"""Convert numbers to words for Indian currency"""


def number_to_words_indian(n: int) -> str:
    """Convert number to words (Indian style)"""
    if n == 0:
        return "Zero"
    
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    tens = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", 
             "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    
    def convert_chunk(num, scale=""):
        if num == 0:
            return ""
        elif num < 10:
            return ones[num] + scale
        elif num < 20:
            return teens[num - 10] + scale
        elif num < 100:
            return tens[num // 10] + " " + ones[num % 10] + scale
        else:
            return ones[num // 100] + " Hundred " + convert_chunk(num % 100, scale)
    
    if n < 1000:
        return convert_chunk(n).strip()
    elif n < 100000:  # Less than 1 lakh
        return (convert_chunk(n // 1000, " Thousand ") + convert_chunk(n % 1000)).strip()
    elif n < 10000000:  # Less than 1 crore
        return (convert_chunk(n // 100000, " Lakh ") + convert_chunk(n % 100000)).strip()
    else:
        return (convert_chunk(n // 10000000, " Crore ") + convert_chunk(n % 10000000)).strip()


def amount_in_words(amount: float) -> str:
    """
    Convert amount to words in Indian format
    
    Example:
        1234.56 -> "One Thousand Two Hundred Thirty Four Rupees and Fifty Six Paise Only"
    """
    rupees = int(amount)
    paise = int(round((amount - rupees) * 100))
    
    result = ""
    
    if rupees > 0:
        result = number_to_words_indian(rupees) + " Rupees"
    
    if paise > 0:
        if rupees > 0:
            result += " and "
        result += number_to_words_indian(paise) + " Paise"
    
    if result:
        result += " Only"
    else:
        result = "Zero Rupees Only"
    
    return result
