from pydantic import BaseModel, Field
from typing import List, Optional

class Socio(BaseModel):
    nome: str = Field(description="Nome completo do sócio.")
    cpf_cnpj: str = Field(description="CPF ou CNPJ do sócio.")
    quantidade_cotas: float
    porcentagem_participacao: float
    e_diretor_administrador: bool = Field(description="true ou false")
    poderes_judiciais_extrajudiciais: bool = Field(description="true ou false")

class Administrador(BaseModel):
    nome: str = Field(description="Nome completo do administrador/diretor.")
    cpf: str = Field(description="CPF do administrador/diretor.")
    prazo_mandato: str = Field(description="Ex: 'Determinado (1 ano)' ou 'Indeterminado'.")
    e_socio: bool = Field(description="true se for sócio, false se for administrador não-sócio.")

class DocumentoSocietario(BaseModel):
    tipo_documento: str
    razao_social: str
    nome_fantasia: Optional[str]
    cnpj: str
    endereco_completo: str
    valor_capital_social: float
    quantidade_cotas_totais: float
    
    socios: List[Socio]
    administradores: List[Administrador] = Field(description="Lista de TODOS os administradores e diretores nomeados no contrato (sócios ou não-sócios).")
    
    forma_assinatura: str
    regras_assinatura: Optional[str]
    
    permite_outorga_procuracao: bool = Field(description="true ou false. Indica se a empresa pode passar procuração.")
    quem_assina_procuracao: Optional[str]
    forma_assinatura_procuracao: Optional[str]
    regras_outorga_procuracao: Optional[str]
    
    data_documento: str
    numero_registro_junta: str
    data_registro: Optional[str]
    
    documento_completo_assinado: bool
    quem_assinou: List[str]