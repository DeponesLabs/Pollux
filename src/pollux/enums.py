from enum import Enum

class GeminiModelType(Enum):
    
    FLASH_1_5 = "gemini-1.5-flash"
    FLASH_2_5 = "gemini-2.5-flash"
    
    PRO_1_5 = "gemini-1.5-pro"
    
    FLASH_3_0_PREVIEW = "gemini-3-flash-preview"
    
    FLASH_LITE_3_1_PREVIEW = "gemini-3.1-flash-lite-preview"
    
    PRO_3_1_PREVIEW = "gemini-3.1-pro-preview"
    
    NANO_BANANA_2 = "gemini-3.1-flash-image-preview"
    NANO_BANANA_PRO = "gemini-3-pro-image-preview"
    
    