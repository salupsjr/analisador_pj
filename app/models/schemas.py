from pydantic import BaseModel, Field
from typing import List, Optional

class Socio(BaseModel):
    nome: str
    cpf_cnpj: str
    quantidade_cotas: float
    porcentagem_participacao: float
    e_diretor_administrador: bool
    poderes_judiciais_extrajudiciais: bool

class DocumentoSocietario(BaseModel):
    tipo_documento: str = Field(description="Ex: Contrato Social, Estatuto, Ata")
    razao_social: str
    nome_fantasia: Optional[str]
    cnpj: str
    endereco_completo: str
    valor_capital_social: float
    quantidade_cotas_totais: float
    socios: List[Socio]
    
    # === CORREÇÃO DA FORMA DE ASSINATURA ===
    forma_assinatura: str = Field(description="Como os administradores assinam pela empresa. Ex: 'Isoladamente', 'Em conjunto'. NUNCA use 'assinatura eletrônica' ou 'digital'.")
    regras_assinatura: Optional[str] = Field(description="Regras específicas de valor ou combinações para assinar.")
    # =======================================
    
    permite_outorga_procuracao: bool
    quem_assina_procuracao: Optional[str]
    forma_assinatura_procuracao: Optional[str] = Field(description="Como os procuradores assinam. Ex: 'Isoladamente', 'Em conjunto'. NUNCA use 'assinatura eletrônica'.")
    regras_outorga_procuracao: Optional[str]
    data_documento: str
    numero_registro_junta: str = Field(description="NIRE ou número de registro na Junta")
    documento_completo_assinado: bool
    quem_assinou: List[str]