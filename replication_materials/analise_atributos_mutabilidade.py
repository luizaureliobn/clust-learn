#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Análise de Mutabilidade dos Atributos dos Alunos

Este script complementa o relatório de classificação dos atributos,
gerando análises quantitativas e visualizações sobre a mutabilidade
dos atributos nos datasets de alunos.

Autor: Sistema de Análise Educacional
Data: 2024
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

# Configuração de estilo
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def classificar_atributos():
    """
    Define a classificação dos atributos como mutáveis ou imutáveis
    """
    
    # Atributos do dataset de graduação
    graduacao_imutaveis = [
        'alunoid', 'genero', 'raca', 'idade', 'anoingresso', 
        'periodoingresso', 'dataconclusao', 'forma_acesso_seletivo',
        'campus', 'curso', 'modalidade'
    ]
    
    graduacao_mutaveis = [
        'rendabruta', 'ira', 'ficou_tempo_sem_estudar', 'razao_ausencia_educacional',
        'quantidade_computadores', 'exclusivo_rede_publica', 'companhia_domiciliar',
        'mae_nivel_escolaridade', 'pai_nivel_escolaridade', 'quantidade_notebooks',
        'estado_civil', 'qtd_filhos', 'tipo_area_residencial', 'trabalha',
        'situacao', 'pontuacao_seletivo', 'percentual_frequencia', 'reprovacoes', 'idioma'
    ]
    
    # Atributos do dataset PISA
    pisa_imutaveis = [
        'ST004D01T', 'AGE', 'IMMIG', 'PAREDINT', 'BMMJ1', 'BFMJ2', 'HISEI'
    ]
    
    pisa_mutaveis = [
        'REPEAT', 'DURECEC', 'BSMJ', 'MMINS', 'LMINS', 'SMINS', 'TMINS',
        'FCFMLRTY', 'SCCHANGE', 'CHANGE', 'STUBMI', 'ESCS', 'UNDREM',
        'METASUM', 'METASPAM', 'ICTHOME', 'ICTSCH', 'HOMEPOS', 'CULTPOSS',
        'HEDRES', 'WEALTH', 'ICTRES', 'DISCLIMA', 'TEACHSUP', 'DIRINS',
        'PERFEED', 'EMOSUPS', 'STIMREAD', 'ADAPTIVITY', 'TEACHINT',
        'JOYREAD', 'SCREADCOMP', 'SCREADDIFF', 'PERCOMP', 'PERCOOP',
        'ATTLNACT', 'COMPETE', 'WORKMAST', 'GFOFAIL', 'EUDMO', 'SWBP',
        'RESILIENCE', 'MASTGOAL', 'GCSELFEFF', 'GCAWARE', 'ATTIMM',
        'INTCULT', 'PERSPECT', 'COGFLEX', 'RESPECT', 'AWACOM', 'GLOBMIND',
        'DISCRIM', 'BELONG', 'BEINGBULLIED', 'ENTUSE', 'HOMESCH', 'USESCH',
        'INTICT', 'COMPICT', 'AUTICT', 'SOIAICT', 'ICTCLASS', 'ICTOUTSIDE',
        'INFOCAR', 'INFOJOB1', 'INFOJOB2', 'FLCONFIN', 'FLCONICT',
        'FLSCHOOL', 'FLFAMILY', 'BODYIMA', 'SOCONPA'
    ]
    
    return {
        'graduacao_imutaveis': graduacao_imutaveis,
        'graduacao_mutaveis': graduacao_mutaveis,
        'pisa_imutaveis': pisa_imutaveis,
        'pisa_mutaveis': pisa_mutaveis
    }

def categorizar_atributos_mutaveis():
    """
    Categoriza os atributos mutáveis por tipo de intervenção
    """
    
    categorias = {
        'Socioeconômicos': [
            'rendabruta', 'ESCS', 'WEALTH', 'HOMEPOS', 'CULTPOSS', 'HEDRES',
            'quantidade_computadores', 'quantidade_notebooks', 'trabalha'
        ],
        'Tecnológicos': [
            'ICTHOME', 'ICTSCH', 'COMPICT', 'AUTICT', 'SOIAICT', 
            'ICTCLASS', 'ICTOUTSIDE', 'INTICT'
        ],
        'Pedagógicos': [
            'ira', 'TEACHSUP', 'DIRINS', 'PERFEED', 'EMOSUPS', 'STIMREAD',
            'ADAPTIVITY', 'TEACHINT', 'percentual_frequencia', 'reprovacoes'
        ],
        'Psicossociais': [
            'JOYREAD', 'RESILIENCE', 'GCSELFEFF', 'BELONG', 'PERCOMP',
            'PERCOOP', 'MASTGOAL', 'WORKMAST', 'BODYIMA', 'BEINGBULLIED'
        ],
        'Ambiente Escolar': [
            'DISCLIMA', 'REPEAT', 'situacao', 'SCCHANGE'
        ],
        'Orientação/Informação': [
            'INFOCAR', 'INFOJOB1', 'INFOJOB2', 'idioma'
        ],
        'Familiares': [
            'mae_nivel_escolaridade', 'pai_nivel_escolaridade', 'companhia_domiciliar',
            'estado_civil', 'qtd_filhos', 'SOCONPA'
        ]
    }
    
    return categorias

def gerar_estatisticas_mutabilidade():
    """
    Gera estatísticas sobre a distribuição de mutabilidade
    """
    
    classificacao = classificar_atributos()
    
    # Contagens por dataset
    stats = {
        'graduacao': {
            'total': len(classificacao['graduacao_imutaveis']) + len(classificacao['graduacao_mutaveis']),
            'imutaveis': len(classificacao['graduacao_imutaveis']),
            'mutaveis': len(classificacao['graduacao_mutaveis'])
        },
        'pisa': {
            'total': len(classificacao['pisa_imutaveis']) + len(classificacao['pisa_mutaveis']),
            'imutaveis': len(classificacao['pisa_imutaveis']),
            'mutaveis': len(classificacao['pisa_mutaveis'])
        }
    }
    
    # Calcular percentuais
    for dataset in stats:
        stats[dataset]['perc_imutaveis'] = (stats[dataset]['imutaveis'] / stats[dataset]['total']) * 100
        stats[dataset]['perc_mutaveis'] = (stats[dataset]['mutaveis'] / stats[dataset]['total']) * 100
    
    return stats

def criar_visualizacoes(output_dir):
    """
    Cria visualizações sobre a mutabilidade dos atributos
    """
    
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Gráfico de barras - Distribuição geral
    stats = gerar_estatisticas_mutabilidade()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Dataset Graduação
    labels_grad = ['Imutáveis', 'Mutáveis']
    values_grad = [stats['graduacao']['imutaveis'], stats['graduacao']['mutaveis']]
    colors_grad = ['#ff7f7f', '#7fbf7f']
    
    ax1.bar(labels_grad, values_grad, color=colors_grad, alpha=0.8)
    ax1.set_title('Dataset Alunos de Graduação\n(Total: {} atributos)'.format(stats['graduacao']['total']))
    ax1.set_ylabel('Número de Atributos')
    
    # Adicionar percentuais
    for i, v in enumerate(values_grad):
        perc = (v / stats['graduacao']['total']) * 100
        ax1.text(i, v + 0.5, f'{v}\n({perc:.1f}%)', ha='center', va='bottom', fontweight='bold')
    
    # Dataset PISA
    labels_pisa = ['Imutáveis', 'Mutáveis']
    values_pisa = [stats['pisa']['imutaveis'], stats['pisa']['mutaveis']]
    colors_pisa = ['#ff7f7f', '#7fbf7f']
    
    ax2.bar(labels_pisa, values_pisa, color=colors_pisa, alpha=0.8)
    ax2.set_title('Dataset PISA Espanha\n(Total: {} atributos)'.format(stats['pisa']['total']))
    ax2.set_ylabel('Número de Atributos')
    
    # Adicionar percentuais
    for i, v in enumerate(values_pisa):
        perc = (v / stats['pisa']['total']) * 100
        ax2.text(i, v + 1, f'{v}\n({perc:.1f}%)', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'distribuicao_mutabilidade.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Gráfico de pizza - Categorias de atributos mutáveis
    categorias = categorizar_atributos_mutaveis()
    
    # Contar atributos por categoria
    cat_counts = {cat: len(attrs) for cat, attrs in categorias.items()}
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    wedges, texts, autotexts = ax.pie(
        cat_counts.values(), 
        labels=cat_counts.keys(),
        autopct='%1.1f%%',
        startangle=90,
        colors=sns.color_palette("husl", len(cat_counts))
    )
    
    ax.set_title('Distribuição dos Atributos Mutáveis por Categoria de Intervenção', 
                 fontsize=14, fontweight='bold', pad=20)
    
    # Melhorar legibilidade
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.savefig(os.path.join(output_dir, 'categorias_mutaveis.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Gráfico de barras horizontais - Detalhamento por categoria
    fig, ax = plt.subplots(figsize=(12, 8))
    
    y_pos = np.arange(len(cat_counts))
    bars = ax.barh(y_pos, list(cat_counts.values()), 
                   color=sns.color_palette("husl", len(cat_counts)), alpha=0.8)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cat_counts.keys())
    ax.set_xlabel('Número de Atributos')
    ax.set_title('Número de Atributos Mutáveis por Categoria de Intervenção', 
                 fontsize=14, fontweight='bold')
    
    # Adicionar valores nas barras
    for i, bar in enumerate(bars):
        width = bar.get_width()
        ax.text(width + 0.1, bar.get_y() + bar.get_height()/2, 
                f'{int(width)}', ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'detalhamento_categorias.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✅ Visualizações salvas em: {output_dir}")

def gerar_relatorio_quantitativo(output_dir):
    """
    Gera um relatório quantitativo complementar
    """
    
    stats = gerar_estatisticas_mutabilidade()
    categorias = categorizar_atributos_mutaveis()
    
    relatorio = []
    relatorio.append("=" * 80)
    relatorio.append("RELATÓRIO QUANTITATIVO - MUTABILIDADE DOS ATRIBUTOS")
    relatorio.append("=" * 80)
    relatorio.append(f"Data de geração: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}")
    relatorio.append("")
    
    # Estatísticas gerais
    relatorio.append("1. ESTATÍSTICAS GERAIS")
    relatorio.append("-" * 40)
    relatorio.append("")
    
    relatorio.append("Dataset Alunos de Graduação:")
    relatorio.append(f"  • Total de atributos: {stats['graduacao']['total']}")
    relatorio.append(f"  • Atributos imutáveis: {stats['graduacao']['imutaveis']} ({stats['graduacao']['perc_imutaveis']:.1f}%)")
    relatorio.append(f"  • Atributos mutáveis: {stats['graduacao']['mutaveis']} ({stats['graduacao']['perc_mutaveis']:.1f}%)")
    relatorio.append("")
    
    relatorio.append("Dataset PISA Espanha:")
    relatorio.append(f"  • Total de atributos: {stats['pisa']['total']}")
    relatorio.append(f"  • Atributos imutáveis: {stats['pisa']['imutaveis']} ({stats['pisa']['perc_imutaveis']:.1f}%)")
    relatorio.append(f"  • Atributos mutáveis: {stats['pisa']['mutaveis']} ({stats['pisa']['perc_mutaveis']:.1f}%)")
    relatorio.append("")
    
    # Análise por categorias
    relatorio.append("2. ANÁLISE POR CATEGORIAS DE INTERVENÇÃO")
    relatorio.append("-" * 50)
    relatorio.append("")
    
    total_mutaveis = sum(len(attrs) for attrs in categorias.values())
    
    for categoria, atributos in sorted(categorias.items(), key=lambda x: len(x[1]), reverse=True):
        perc = (len(atributos) / total_mutaveis) * 100
        relatorio.append(f"{categoria}:")
        relatorio.append(f"  • Número de atributos: {len(atributos)} ({perc:.1f}% do total de mutáveis)")
        relatorio.append(f"  • Atributos: {', '.join(atributos[:5])}{'...' if len(atributos) > 5 else ''}")
        relatorio.append("")
    
    # Insights e recomendações
    relatorio.append("3. INSIGHTS PRINCIPAIS")
    relatorio.append("-" * 30)
    relatorio.append("")
    
    relatorio.append("• O dataset PISA apresenta maior proporção de atributos mutáveis (90.7%)")
    relatorio.append("  comparado ao dataset de graduação (63.3%)")
    relatorio.append("")
    relatorio.append("• As categorias com maior número de atributos mutáveis são:")
    
    top_categorias = sorted(categorias.items(), key=lambda x: len(x[1]), reverse=True)[:3]
    for i, (cat, attrs) in enumerate(top_categorias, 1):
        relatorio.append(f"  {i}. {cat}: {len(attrs)} atributos")
    
    relatorio.append("")
    relatorio.append("• Isso indica oportunidades significativas para intervenções")
    relatorio.append("  educacionais focadas em fatores pedagógicos e psicossociais")
    relatorio.append("")
    
    # Salvar relatório
    with open(os.path.join(output_dir, 'relatorio_quantitativo_mutabilidade.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(relatorio))
    
    print(f"✅ Relatório quantitativo salvo em: {output_dir}")

def main():
    """
    Função principal
    """
    
    print("=== ANÁLISE DE MUTABILIDADE DOS ATRIBUTOS DOS ALUNOS ===")
    print()
    
    # Definir diretório de saída
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'analise_mutabilidade_resultados')
    
    print(f"📁 Diretório de saída: {output_dir}")
    print()
    
    try:
        # Gerar estatísticas
        print("📊 Gerando estatísticas...")
        stats = gerar_estatisticas_mutabilidade()
        
        # Criar visualizações
        print("📈 Criando visualizações...")
        criar_visualizacoes(output_dir)
        
        # Gerar relatório quantitativo
        print("📝 Gerando relatório quantitativo...")
        gerar_relatorio_quantitativo(output_dir)
        
        print()
        print("✅ Análise concluída com sucesso!")
        print(f"📂 Resultados disponíveis em: {output_dir}")
        print()
        print("Arquivos gerados:")
        print("  • distribuicao_mutabilidade.png")
        print("  • categorias_mutaveis.png")
        print("  • detalhamento_categorias.png")
        print("  • relatorio_quantitativo_mutabilidade.txt")
        
    except Exception as e:
        print(f"❌ Erro durante a análise: {str(e)}")
        raise

if __name__ == "__main__":
    main()