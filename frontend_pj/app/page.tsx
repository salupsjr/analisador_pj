"use client";

import { useState } from "react";
import { UploadCloud, Building2, Users, FileSignature, AlertTriangle, Loader2, UserCheck } from "lucide-react";

export default function DashboardIDP() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [erro, setErro] = useState("");
  const [dados, setDados] = useState<any>(null);

  const processarDocumento = async () => {
    if (!file) {
      setErro("Por favor, selecione um arquivo PDF primeiro.");
      return;
    }
    setLoading(true);
    setErro("");
    setDados(null);

    const formData = new FormData();
    formData.append("arquivo", file);

    try {
      const res = await fetch("http://localhost:8000/extrair", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Erro ao conectar com o motor de IA.");
      }

      setDados(data);
    } catch (err: any) {
      setErro(err.message || "Falha de conexão. O servidor Python está rodando na porta 8000?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-100 p-8 text-neutral-800 font-sans">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Cabeçalho */}
        <div className="border-b border-neutral-200 pb-4">
          <h1 className="text-3xl font-bold text-neutral-900">Análise de Firmas e Poderes</h1>
          <p className="text-neutral-500">Extração automatizada e validação de regras societárias.</p>
        </div>

        {/* Alerta de Erro */}
        {erro && (
          <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded shadow-sm flex items-center gap-3">
            <AlertTriangle className="w-5 h-5" />
            <p>{erro}</p>
          </div>
        )}

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Coluna Esquerda - Upload */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-xl shadow-sm border border-neutral-200">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <UploadCloud className="w-5 h-5 text-blue-600" /> Upload de Documento
              </h2>
              <div className="border-2 border-dashed border-neutral-300 rounded-lg p-8 flex flex-col items-center justify-center bg-neutral-50 hover:bg-neutral-100 transition-colors">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={(e) => setFile(e.target.files?.[0] || null)}
                  className="w-full text-sm text-neutral-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
                />
              </div>
              <button
                onClick={processarDocumento}
                disabled={loading || !file}
                className="w-full mt-6 bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-lg flex justify-center items-center gap-2 disabled:bg-blue-300 transition-colors"
              >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Processar Documento"}
              </button>
            </div>
          </div>

          {/* Coluna Direita - Cards de Resultados */}
          <div className="lg:col-span-2 space-y-6">
            {!dados && !loading && (
              <div className="bg-white p-12 rounded-xl shadow-sm border border-neutral-200 flex flex-col items-center justify-center text-center text-neutral-400 h-full min-h-[400px]">
                <FileSignature className="w-12 h-12 mb-4 opacity-50" />
                <p>Nenhum documento processado.</p>
                <p className="text-sm mt-1">Faça o upload de um Contrato Social para visualizar os dados.</p>
              </div>
            )}

            {loading && (
              <div className="bg-white p-12 rounded-xl shadow-sm border border-neutral-200 flex flex-col items-center justify-center text-center text-neutral-400 h-full min-h-[400px]">
                <Loader2 className="w-10 h-10 animate-spin text-blue-600 mb-4" />
                <p className="text-neutral-600 font-medium animate-pulse">A IA está lendo o documento...</p>
              </div>
            )}

            {dados && (
              <>
                {/* Alerta Matemático (Regra de Negócio) */}
                {dados.ALERTA_VALIDACAO && (
                  <div className="bg-amber-100 border-l-4 border-amber-500 text-amber-800 p-4 rounded-lg shadow-sm flex items-start gap-3">
                    <AlertTriangle className="w-6 h-6 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="font-bold">Alerta de Validação Societária</h4>
                      <p className="text-sm">{dados.ALERTA_VALIDACAO}</p>
                    </div>
                  </div>
                )}

                {/* Card 1: Dados da Empresa */}
                <div className="bg-white rounded-xl shadow-sm border border-neutral-200 overflow-hidden">
                  <div className="bg-neutral-800 px-6 py-4 flex items-center gap-2 text-white">
                    <Building2 className="w-5 h-5" />
                    <h3 className="font-semibold text-lg">Dados da Empresa</h3>
                  </div>
                  <div className="p-6 grid grid-cols-2 lg:grid-cols-3 gap-y-4 gap-x-6">
                    <div className="col-span-2 lg:col-span-3"><p className="text-xs text-neutral-500 uppercase font-semibold">Razão Social</p><p className="font-medium">{dados.razao_social}</p></div>
                    <div><p className="text-xs text-neutral-500 uppercase font-semibold">CNPJ</p><p className="font-medium">{dados.cnpj}</p></div>
                    <div><p className="text-xs text-neutral-500 uppercase font-semibold">Reg. Junta (Não é NIRE)</p><p className="font-medium">{dados.numero_registro_junta}</p></div>
                    <div><p className="text-xs text-neutral-500 uppercase font-semibold">Data Registro</p><p className="font-medium">{dados.data_registro || '-'}</p></div>
                    <div className="col-span-2 lg:col-span-3"><p className="text-xs text-neutral-500 uppercase font-semibold">Capital Social</p><p className="font-medium">R$ {dados.valor_capital_social?.toLocaleString('pt-BR')}</p></div>
                  </div>
                </div>

                {/* Card 2: Quadro Societário (Sócios) */}
                <div className="bg-white rounded-xl shadow-sm border border-neutral-200 overflow-hidden">
                  <div className="bg-neutral-800 px-6 py-4 flex items-center gap-2 text-white">
                    <Users className="w-5 h-5" />
                    <h3 className="font-semibold text-lg">Quadro Societário</h3>
                  </div>
                  <div className="p-0 overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                      <thead>
                        <tr className="bg-neutral-50 border-b border-neutral-200 text-xs uppercase text-neutral-500">
                          <th className="px-6 py-3 font-semibold">Nome</th>
                          <th className="px-6 py-3 font-semibold">CPF/CNPJ</th>
                          <th className="px-6 py-3 font-semibold">% Cotas</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-neutral-100">
                        {dados.socios?.map((socio: any, idx: number) => (
                          <tr key={idx} className="hover:bg-neutral-50">
                            <td className="px-6 py-4 font-medium">{socio.nome}</td>
                            <td className="px-6 py-4 text-neutral-600">{socio.cpf_cnpj}</td>
                            <td className="px-6 py-4">{socio.porcentagem_participacao}%</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* NOVO Card 3: Administradores e Diretores */}
                <div className="bg-white rounded-xl shadow-sm border border-neutral-200 overflow-hidden">
                  <div className="bg-neutral-800 px-6 py-4 flex items-center gap-2 text-white">
                    <UserCheck className="w-5 h-5" />
                    <h3 className="font-semibold text-lg">Administradores | Diretores</h3>
                  </div>
                  <div className="p-0 overflow-x-auto">
                    <table className="w-full text-left border-collapse">
                      <thead>
                        <tr className="bg-neutral-50 border-b border-neutral-200 text-xs uppercase text-neutral-500">
                          <th className="px-6 py-3 font-semibold">Nome</th>
                          <th className="px-6 py-3 font-semibold">CPF</th>
                          <th className="px-6 py-3 font-semibold">Mandato</th>
                          <th className="px-6 py-3 font-semibold">É Sócio?</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-neutral-100">
                        {dados.administradores?.map((admin: any, idx: number) => (
                          <tr key={idx} className="hover:bg-neutral-50">
                            <td className="px-6 py-4 font-medium">{admin.nome}</td>
                            <td className="px-6 py-4 text-neutral-600">{admin.cpf}</td>
                            <td className="px-6 py-4 text-neutral-600">{admin.prazo_mandato}</td>
                            <td className="px-6 py-4">
                              <span translate="no" className={`px-2 py-1 rounded-full text-xs font-semibold ${admin.e_socio ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'}`}>
                                {admin.e_socio ? 'SIM' : 'NÃO'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Card 4: Governança e Procurações */}
                <div className="bg-white rounded-xl shadow-sm border border-neutral-200 overflow-hidden">
                  <div className="bg-neutral-800 px-6 py-4 flex items-center gap-2 text-white">
                    <FileSignature className="w-5 h-5" />
                    <h3 className="font-semibold text-lg">Governança e Procurações</h3>
                  </div>
                  <div className="p-6 space-y-4">
                    <div className="bg-blue-50 p-4 rounded border border-blue-100">
                      <p className="text-xs text-blue-600 uppercase font-bold mb-1">Forma de Assinatura (Empresa)</p>
                      <p className="text-blue-900 font-medium">{dados.forma_assinatura}</p>
                    </div>
                    <div>
                      <p className="text-xs text-neutral-500 uppercase font-semibold">Permite Procuração?</p>
                      <p translate="no" className="font-medium text-lg">
                        {dados.permite_outorga_procuracao ? 'SIM' : 'NÃO'}
                      </p>
                    </div>
                    {dados.permite_outorga_procuracao && (
                      <>
                        <div>
                          <p className="text-xs text-neutral-500 uppercase font-semibold">QUEM DEVE ASSINAR PROCURAÇÃO</p>
                          <p className="font-medium text-neutral-700">{dados.quem_assina_procuracao || '-'}</p>
                        </div>
                        <div>
                          <p className="text-xs text-neutral-500 uppercase font-semibold">Forma de Assinatura (Procuração)</p>
                          <p className="font-medium text-neutral-700">{dados.forma_assinatura_procuracao || '-'}</p>
                        </div>
                        {dados.regras_outorga_procuracao && (
                          <div className="pt-2 border-t border-neutral-100 mt-2">
                            <p className="text-xs text-neutral-500 uppercase font-semibold">Observações / Regras</p>
                            <p className="text-sm text-neutral-600 italic mt-1">{dados.regras_outorga_procuracao}</p>
                          </div>
                        )}
                      </>
                    )}
                  </div>
                </div>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}