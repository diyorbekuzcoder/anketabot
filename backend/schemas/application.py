from pydantic import BaseModel, Field
from typing import Optional

class AnketaFormModel(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = "mavjud emas"
    
    # 1. Asosiy ma'lumotlar
    ism: str = Field(..., description="Ism")
    familiya: str = Field(..., description="Familiya")
    otasining_ismi: str = Field(..., description="Otasining ismi")
    tugilgan_sana: str = Field(..., description="Tug'ilgan sana")
    jins: str = Field(..., description="Jins")
    oilaviy_holati: str = Field(..., description="Oilaviy holati")
    
    # 2. Ta'lim va tillar
    malumoti: str = Field(..., description="Ma'lumoti")
    talabami: str = Field(..., description="Talabami")
    
    # 3. Jismoniy va manzil
    boy: int = Field(..., description="Bo'yi (sm)")
    vazn: int = Field(..., description="Vazn (kg)")
    viloyat: str = Field(..., description="Viloyat")
    tuman: str = Field(..., description="Tuman")
    manzil_toliq: str = Field(..., description="To'liq manzil")
    filial: str = Field(..., description="Filial")
    lavozim: str = Field(..., description="Lavozim")
    
    # 4. Ish holati
    avval_ishlagan: str = Field(..., description="Avval ishlaganmi")
    fuqaro: str = Field(..., description="Fuqaro")
    ishlaydimi: str = Field(..., description="Hozir ishlaydimi")
    avto: str = Field(..., description="Avto bormi")
    xizmat_safari: str = Field(..., description="Xizmat safari")
    qarindoshlar: str = Field("Yoq", description="Qarindoshlar")
    
    # 5. Sog'liq va tajriba
    sogliq_ogir_narsa: str = Field(..., description="Og'ir yuk ko'tara oladimi")
    sogliq_ogir_narsa_izoh: Optional[str] = None
    sogliq_yurak: str = Field(..., description="Yurak kasalligi")
    sogliq_yurak_izoh: Optional[str] = None
    sogliq_jarrohlik: str = Field(..., description="Jarrohlik o'tkazganmi")
    sogliq_jarrohlik_izoh: Optional[str] = None
    sogliq_koz: str = Field(..., description="Ko'rish qobiliyati")
    sogliq_koz_izoh: Optional[str] = None
    sogliq_bel: str = Field(..., description="Bel og'rig'i")
    sogliq_bel_izoh: Optional[str] = None
    sogliq_joyida_ishlash: str = Field(..., description="O'tirib ishlash qobiliyati")
    sogliq_joyida_ishlash_izoh: Optional[str] = None
    
    oxirgi_maosh: int = Field(..., description="Oxirgi maosh (so'm)")
    xohlagan_maosh: int = Field(..., description="Xohlagan maosh (so'm)")
    qayerdan_bildi: str = Field(..., description="Biz haqimizda qayerdan bildi")
    sudlanganlik: str = Field(..., description="Sudlanganlik holati")
    qoshimcha_izoh: str = Field("Yoq", description="Qo'shimcha izoh")
    
    # 6. Aloqa va hujjat
    qoshimcha_tel: str = Field("Yoq", description="Qo'shimcha tel")
    pasport_turi: str = Field(..., description="Pasport turi")
