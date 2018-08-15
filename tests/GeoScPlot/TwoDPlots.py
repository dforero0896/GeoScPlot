#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Este código pretende facilitar la diagramación de discriminantes geoquímicos a partir de análisis de esta
índole. Para probar este código se toman los datos utilizados en los cursos de Geoquímica (Semestre 201510) y
Petrología (Semestre 201620) del programa de Geociencias en la Universidad de los Andes, Bogotá, Colombia.
Distintos discriminantes son utilizados, la bibliografía asociada puede ser consultada en mi propio informe de
Petrología.'''

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pkg_resources

DATA_PATH = pkg_resources.resource_filename('GeoScPlot','data/')
def convertToAnhBase(data):
    '''Returns properly arranged DataFrame "data" into anhidrous base data'''
    muestras = data.index
    majorElemsWLOI = data.loc[:,str(data.columns[0]):'LOI']
    majorElems = majorElemsWLOI.drop(columns='LOI')
    sumLOI = majorElemsWLOI.sum(axis=1)
    sumNoLOI = majorElems.sum(axis=1)
    anhBase = majorElems.copy()
    for col in majorElems.columns:
        anhBase[col] = majorElems[col]/(sumNoLOI/sumLOI)
    return anhBase.astype(float)
def buildTas():
    '''Returns the TAS format in an (fig, ax) object.'''
    TAS, ax=plt.subplots(1, 1, figsize=(10, 7))
    filenames = [DATA_PATH+'TAS_0'+str(i)+'.csv' for i in range(1,7)]
    datasets = [np.loadtxt(fileN, delimiter=',', dtype=float) for fileN in filenames]
    [ax.plot(data[:,0], data[:,1], c='k', lw=3) for data in datasets]
    blue = np.loadtxt(DATA_PATH+'/TAS_blue.csv', delimiter=',', dtype=float)
    ax.plot(blue[:,0], blue[:,1], c='b', lw=3)
    ax.text(41, 0, 'picro-\nbasalto',fontsize=12)
    ax.text(46, 0.5, 'basalto',fontsize=12)
    ax.text(52, 1.3, u'andesita\nbasáltica',fontsize=12)
    ax.text(57, 3.2, 'andesita',fontsize=12)
    ax.text(67, 4, 'dacita',fontsize=12)
    ax.text(70, 8.4, 'riolita',fontsize=12)
    ax.text(75, 9.1, 'subalcalina',fontsize=15, color='b')
    ax.text(62, 9.4, 'alcalina',fontsize=15, color='b')
    ax.text(47, 5.1, 'traqui\nbasalto',fontsize=12)
    ax.text(50, 6.5, u'traqui-andesita\nbasáltica',fontsize=12)
    ax.text(53, 9, 'traqui-andesita',fontsize=12)
    ax.text(41, 6.2, 'tefrita\nbasanita',fontsize=12)
    ax.text(47, 8.9, 'tefro-\nfonolita',fontsize=12)
    ax.text(50, 11, 'fono-\ntefrita',fontsize=12)
    ax.text(37, 9.8, 'foidita',fontsize=12)
    ax.text(51, 15, 'fonolita',fontsize=12)
    ax.text(60, 13, 'traquita',fontsize=12)
    ax.text(60, 11, 'traqui-\ndacita',fontsize=12)
    ax.set_xlim((35, 85))
    ax.set_ylim((0, 16))
    ax.set_xlabel("$SiO_2(wt\%)$", fontsize=30)
    ax.set_ylabel("$K_2O+Na_2O(wt\%)$", fontsize=30)
    ax.set_aspect(2)
    return TAS, ax
def plotTAS(data, save=False, nombre = 'TAS'):
    '''Guarda el diagrama TAS dado un set de datos como pandas DataFrame.'''
    muestras = data.index
    loscolores=["lawngreen", "cyan", "gold", "fuchsia", "r", "indigo"]
    anhBase = convertToAnhBase(data)
    Alk = anhBase['K2O']+anhBase['Na2O']
    SiO2 = anhBase['SiO2']
    TAS, ax = buildTas()
    ax.scatter(SiO2, Alk, c=loscolores, s=100)
    for i, txt in enumerate(muestras):
        ax.annotate(txt, (SiO2[i]+0.7,Alk[i]), fontsize=10)
    if save:
        plt.tight_layout()
        plt.gcf()
        plt.savefig(nombre+'.png', dpi=300)

def plotHarker(data, save=False, nombre = 'Harker'):
    muestras = data.index
    loscolores=["lawngreen", "cyan", "gold", "fuchsia", "r", "indigo"]
    anhBase = convertToAnhBase(data)
    Final, axes =plt.subplots(3, 2, figsize=(20, 20))
    Final.set_tight_layout()
    axes[0, 0].scatter(anhBase['SiO2'], anhBase['Al2O3'], c=anhBase['CaO'], s=100)
    axes[0, 0].grid()
    axes[0, 0].set_xlabel("$SiO_2(wt\%)$", fontsize=25)
    axes[0, 0].set_ylabel("$Al_2O_3(wt\%)$", fontsize=25)
    mAl, bAl, r_valueAl, p_valueAl, std_errAl = stats.linregress(anhBase['SiO2'], anhBase['Al2O3'])
    axes[0, 0].plot(anhBase['SiO2'], mAl*anhBase['SiO2']+bAl, c="r", ls="-.", lw=3)
    for i, txt in enumerate(muestras):
        axes[0, 0].annotate(txt, (anhBase['SiO2'][i]+0.03,anhBase['Al2O3'][i]+0.01))
    axes[0, 1].scatter(anhBase['SiO2'], anhBase['TiO2'], c=anhBase['CaO'], s=100)
    axes[0, 1].grid()
    axes[0, 1].set_xlabel("$SiO_2(wt\%)$", fontsize=25)
    axes[0, 1].set_ylabel("$TiO_2(wt\%)$", fontsize=25)
    mFe, bFe, r_valueFe, p_valueFe, std_errFe = stats.linregress(anhBase['SiO2'], anhBase['TiO2'])
    axes[0, 1].plot(anhBase['SiO2'], mFe*anhBase['SiO2']+bFe, c="r", ls="-.", lw=3)
    for i, txt in enumerate(muestras):
        axes[0, 1].annotate(txt, (anhBase['SiO2'][i]+0.03,anhBase['TiO2'][i]+0.01))
    axes[1, 0].scatter(anhBase['SiO2'], anhBase['MgO'], c=anhBase['CaO'], s=100)
    axes[1, 0].grid()
    axes[1, 0].set_xlabel("$SiO_2(wt\%)$", fontsize=25)
    axes[1, 0].set_ylabel("$MgO(wt\%)$", fontsize=25)
    mMg, bMg, r_valueMg, p_valueMg, std_errMg = stats.linregress(anhBase['SiO2'], anhBase['MgO'])
    axes[1, 0].plot(anhBase['SiO2'], mMg*anhBase['SiO2']+bMg, c="r", ls="-.", lw=3)
    for i, txt in enumerate(muestras):
        axes[1, 0].annotate(txt, (anhBase['SiO2'][i]+0.03,anhBase['MgO'][i]+0.01))
    axes[1, 1].scatter(anhBase['SiO2'], anhBase['CaO'], c=anhBase['CaO'], s=100)
    axes[1, 1].grid()
    axes[1, 1].set_xlabel("$SiO_2(wt\%)$", fontsize=25)
    axes[1, 1].set_ylabel("$'CaO'](wt\%)$", fontsize=25)
    mCa, bCa, r_valueCa, p_valueCa, std_errCa = stats.linregress(anhBase['SiO2'], anhBase['CaO'])
    axes[1, 1].plot(anhBase['SiO2'], mCa*anhBase['SiO2']+bCa, c="r", ls="-.", lw=3)
    for i, txt in enumerate(muestras):
        axes[1, 1].annotate(txt, (anhBase['SiO2'][i]+0.03,anhBase['CaO'][i]+0.01))
    axes[2, 0].scatter(anhBase['SiO2'], anhBase['K2O'], c=anhBase['CaO'], s=100)
    axes[2, 0].grid()
    axes[2, 0].set_xlabel("$SiO_2(wt\%)$", fontsize=25)
    axes[2, 0].set_ylabel("$K_2O(wt\%)$", fontsize=25)
    mK, bK, r_valueK, p_valueK, std_errK = stats.linregress(anhBase['SiO2'], anhBase['K2O'])
    axes[2, 0].plot(anhBase['SiO2'], mK*anhBase['SiO2']+bK, c="r", ls="-.", lw=3)
    for i, txt in enumerate(muestras):
        axes[2, 0].annotate(txt, (anhBase['SiO2'][i]+0.03,anhBase['K2O'][i]+0.01))
    axes[2, 1].scatter(anhBase['SiO2'], anhBase['Na2O'], c=anhBase['CaO'], s=100)
    axes[2, 1].grid()
    axes[2, 1].set_xlabel("$SiO_2(wt\%)$", fontsize=25)
    axes[2, 1].set_ylabel("$Na_2O(wt\%)$", fontsize=25)
    mNa, bNa, r_valueNa, p_valueNa, std_errNa = stats.linregress(anhBase['SiO2'], anhBase['Na2O'])
    axes[2, 1].plot(anhBase['SiO2'], mNa*anhBase['SiO2']+bNa, c="r", ls="-.", lw=3)
    for i, txt in enumerate(muestras):
        axes[2, 1].annotate(txt, (anhBase['SiO2'][i]+0.03,anhBase['Na2O'][i]+0.01))
    Final.subplots_adjust(hspace=0.3, wspace=0.3)
    if save:
        plt.tight_layout()
        plt.gcf()
        plt.savefig(nombre+'.png', dpi=300)
def buildZrTi_NbY():
    '''Builds the Zr/Ti vs. Nb/Y format in the given axis "ax"'''
    YNb, ax=plt.subplots(1, 1, figsize=(10, 7))
    filenames = [DATA_PATH+'Zr0'+str(i)+'.csv' for i in range(1,10)]
    datasets = [np.loadtxt(fileN, delimiter=',', dtype=float) for fileN in filenames]
    [ax.plot(data[:,0], data[:,1], c='k', lw=3) for data in datasets]
    ax.text(1.1e-2, 5e-3,'Andesita/\nBasalto', fontsize=15)
    ax.text(7e-2, 1.1e-3,'Basalto\nSubalcalino', fontsize=15)
    ax.text(7e-1, 1.5e-3,'Basalto\nAlcalino', fontsize=15)
    ax.text(3e0, 7e-3,'Basanita\nNefelinita', fontsize=15)
    ax.text(7e-1, 3e-2,'Traqui-\nandesita', fontsize=15)
    ax.text(3e-2, 2e-2,'Andesita', fontsize=15)
    ax.text(3.5e-2, 6e-2,'Riodacita\nDacita', fontsize=15)
    ax.text(1.8e-1, 1.5e-1,'Riolita', fontsize=15)
    ax.text(1.8e0, 1e-1,'Traquita', fontsize=15)
    ax.text(1.5e-1, 3e0,'Comptonita', fontsize=15)
    ax.text(3e0, 1e0,'Fonolita', fontsize=15)
    ax.set_xlim((0.01, 10))
    ax.set_ylim((0.001, 10))
    ax.set_ylabel("$Zr/TiO_2*0.0001$", fontsize=30)
    ax.set_xlabel("$Nb/Y$", fontsize=30)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_aspect(0.4)
    return YNb, ax
def plotZrTi_NbY(data, save=False, nombre = 'ZrTi_NbY'):
    data = data.astype(float)
    muestras = data.index
    loscolores=["lawngreen", "cyan", "gold", "fuchsia", "r", "indigo"]
    ZrTi = 1e-4*data['Zr']/data['TiO2']
    NbY = data['Nb']/data['Y']
    YNb, ax=buildZrTi_NbY()
    ax.scatter(NbY, ZrTi, c=loscolores, s=100)
    for i, txt in enumerate(muestras):
        ax.annotate(txt, (NbY[i]+0.005,ZrTi[i]-0.001), fontsize=12)
    if save:
        plt.tight_layout()
        plt.gcf()
        plt.savefig(nombre+'.png', dpi=300)
def plotREE(data, save=False, nombre = 'REE'):
    elementos=["La", "Ce", "Pr", "Nd", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu"]
    loscolores=["lawngreen", "cyan", "gold", "fuchsia", "r", "indigo"]
    ree = data.loc[:,'LOI':]
    ree = ree[elementos]
    condrito = pd.read_csv('Condrito_McDonoughSun95.csv', sep=',')
    condrito = condrito.set_index(condrito['elem'], drop=True).drop(columns='elem').transpose()
    condrito = condrito[elementos]
    condrito=condrito.transpose()
    ree = ree.transpose()
    muestras = ree.columns
    colorDict = dict(zip(muestras,loscolores[:len(muestras)]))
    REE, ax=plt.subplots(1, 1, figsize=(15, 7))
    ax.set_yscale("log")
    ax.set_ylim(1, 1000)
    ax.set_xlim(0, len(ree.index)+1)
    ax.set_ylabel("$Roca/Condrito$", fontsize=30)
    num = np.arange(1,len(ree.index)+1)
    plt.xticks(np.arange(min(num), max(num)+1, 1.0))
    for sample in muestras:
        norm = ree[sample]/condrito['conc']
        ax.plot(num,norm, 'o-', c=colorDict[sample], lw=2, label = sample)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.set_xticklabels([e for e in ree.index], fontsize=20)
    ax.legend(loc=0, fontsize=15)
    REE.canvas.draw()
    if save:
        plt.tight_layout()
        plt.gcf()
        plt.savefig(nombre+'.png', dpi=300)
def plotSpider(data, save=False, nombre = 'Spider'):
    loscolores=["lawngreen", "cyan", "gold", "fuchsia", "r", "indigo"]
    elementos=["Cs", "Rb", "Ba", "Th", "U", "Nb", "Ta", "La", "Ce", "Pb", "Pr", "Sr", "Nd", "Zr", "Sm", "Eu", "Gd", "Tb", "Dy", "Y", "Ho", "Er", "Yb", "Lu"]
    ree = data.loc[:,'LOI':]
    ree = ree[elementos]
    morb = pd.read_csv('MORB_SunMcDonough89.csv', sep=',')
    morb = morb.set_index(morb['elem'], drop=True).drop(columns='elem').transpose()
    morb = morb[elementos]
    morb=morb.transpose()
    ree = ree.transpose()
    muestras = ree.columns
    colorDict = dict(zip(muestras,loscolores[:len(muestras)]))
    REE, ax=plt.subplots(1, 1, figsize=(15, 7))
    ax.set_yscale("log")
    ax.set_ylim(0.01, 1000)
    ax.set_xlim(0, len(ree.index)+1)
    ax.set_ylabel("$Roca/N-MORB$", fontsize=30)
    num = np.arange(1,len(ree.index)+1)
    plt.xticks(np.arange(min(num), max(num)+1, 1.0))
    for sample in muestras:
        norm = ree[sample]/morb['conc']
        ax.plot(num,norm, 'o-', c=colorDict[sample], lw=2, label = sample)
    ax.tick_params(axis='x', labelsize=15)
    ax.tick_params(axis='y', labelsize=15)
    ax.set_xticklabels([e for e in ree.index], fontsize=20)
    ax.legend(loc=0, fontsize=15)
    REE.canvas.draw()
    if save:
        plt.tight_layout()
        plt.gcf()
        plt.savefig(nombre+'.png', dpi=300)
def buildShervais():
    '''Builds the Shervais V vs. Ti discriminant format in the given axis "ax"'''
    Shervais, ax=plt.subplots(1, 1, figsize=(10, 7))
    black = np.loadtxt(DATA_PATH+'Shervais_black.csv',delimiter=',', dtype=float)
    blue = np.loadtxt(DATA_PATH+'Shervais_blue.csv',delimiter=',', dtype=float)
    red = np.loadtxt(DATA_PATH+'Shervais_red.csv',delimiter=',', dtype=float)
    ax.plot(black[:2,0],black[:2,1], c='k', lw=3)
    ax.plot([black[0,0],black[2,0]],[black[0,1],black[2,1]], c='k', lw=3)
    ax.plot([black[0,0],black[3,0]],[black[0,1],black[3,1]], c='k', lw=3)
    ax.plot([black[0,0],black[4,0]],[black[0,1],black[4,1]], c='k', lw=3)
    ax.plot(blue[:,0], blue[:,1],'o', c='b', lw=3)
    ax.plot(red[:,0], red[:,1],'o', c='r', lw=3)
    ax.text(np.mean(blue[:,0])-1, np.mean(blue[:,1])+50, 'Boninites', fontsize=15, rotation=70)
    ax.text(np.mean(red[:,0])-1.5, np.mean(red[:,1])+80, 'Calc-alkaline and\nshoshonitic rocks', fontsize=15, rotation=70)
    ax.text(7.5, 550, 'Arc\ntholeiites', fontsize=15)
    ax.text(17.5, 550, 'Flood Basalts', fontsize=15)
    ax.text(17.5, 250, 'Ocean island and\nalkali basalts', fontsize=15)
    ax.text(7.5, 450, 'B a c k   a r c   b a s i n s', fontsize=15)
    ax.set_xlim((-0, 25.5))
    ax.set_ylim((-0.5, 650))
    #img = plt.imread(".temps/Shervais(0, 30000).png")
    ax.set_ylabel("$V (ppm)$", fontsize=30)
    ax.set_xlabel("$Ti (ppm)/1000$", fontsize=30)
    ax.set_aspect(0.027)
    return Shervais, ax

def plotShervais(data, save=False, nombre = 'Shervais'):
    muestras = data.index
    loscolores=["lawngreen", "cyan", "gold", "fuchsia", "r", "indigo"]
    Vanad = data['V']
    TiO2 = data['TiO2']
    mTi = 47.86
    mO = 16.
    Titan = TiO2*1e4*mTi/(2*mO+mTi)
    Shervais, ax = buildShervais()
    ax.scatter(Titan/1e3, Vanad, c=loscolores, s=100)
    for i, txt in enumerate(muestras):
        ax.annotate(txt, (Titan[i]/1000+0.1,Vanad[i]+0))
    if save:
        plt.tight_layout()
        plt.gcf()
        plt.savefig(nombre+'.png', dpi=300)
def buildThTa():
    '''Builds the Th/Yb vs. Ta/Yb discriminant format in the given axis "ax"'''
    ThYb, ax=plt.subplots(1, 1, figsize=(10, 7))
    ThTa = np.loadtxt(DATA_PATH+'ThTa.csv', delimiter=',', dtype=float)
    print len(ThTa[:2,0])
    ax.plot(ThTa[0:2,0],ThTa[0:2,1], c='k', lw=3)
    ax.plot(ThTa[2:4,0],ThTa[2:4,1], c='b', lw=4)
    ax.plot(ThTa[4:6,0],ThTa[4:6,1], c='r', lw=4)
    ax.plot(ThTa[6:8,0],ThTa[6:8,1], c='r', lw=4)
    ax.plot(ThTa[8:,0],ThTa[8:,1], c='r', lw=3)
    ax.text(2e-2, 4, 'Shoshonitic', fontsize=15)
    ax.text(2e-1, 4, 'Medium to high-K\n calc-alkaline', fontsize=15)
    ax.text(3, 4, 'Enriched\nMantle', fontsize=15)
    ax.text(2e-2, 0.4, 'Low-K calc-\nalkaline arc', fontsize=15)
    ax.text(1.5e-2, 0.13, 'Calc-alkaline', fontsize=15)
    ax.text(0.12, 0.5, 'Active continental\nmargin and alkalic\nocen arcs', fontsize=10, rotation=90)
    ax.text(0.09, 0.5, 'Oceanic arcs', fontsize=10, rotation=90)
    ax.set_xlim((0.01, 10))
    ax.set_ylim((0.01, 10))
    ax.set_ylabel("$Th/Yb$", fontsize=30)
    ax.set_xlabel("$Ta/Yb$", fontsize=30)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_aspect(0.8)
    return ThYb, ax
def plotThTa(data, save=False, nombre = 'ThTa'):
    muestras = data.index
    loscolores=["lawngreen", "cyan", "gold", "fuchsia", "r", "indigo"]
    Th = data['Th']
    Ta = data['Ta']
    Yb = data['Yb']
    Th/=Yb
    Ta/=Yb
    ThYb, ax = buildThTa()
    ax.scatter(Ta, Th, c=loscolores, s=100)
    if save:
        plt.tight_layout()
        plt.gcf()
        plt.savefig(nombre+'.png', dpi=300)

def buildPierce():
    '''Builds the Pierce's Ti vs. Zr discriminant format in the given axis "ax"'''
    PearceDiscrimin, ax=plt.subplots(1, 1, figsize=(10, 7))

    arcLavas=np.loadtxt(DATA_PATH+'arcLavas.csv', delimiter=',', dtype=float)
    withinPlateLavas=np.loadtxt(DATA_PATH+'withinPlateLavas.csv', delimiter=',', dtype=float)
    morbLavas=np.loadtxt(DATA_PATH+'morbLavas.csv', delimiter=',', dtype=float)
    ax.plot(arcLavas[:,0], arcLavas[:,1], lw=3)
    ax.text(np.mean(arcLavas[:,0]), np.mean(arcLavas[:,1]), 'Arc Lavas', fontsize=15)
    ax.plot(morbLavas[:,0], morbLavas[:,1], lw=3)
    ax.text(50, 5000, 'MORB', fontsize=15)
    ax.plot(withinPlateLavas[:,0], withinPlateLavas[:,1], lw=3)
    ax.text(np.mean(withinPlateLavas[:,0])-200, np.mean(withinPlateLavas[:,1])+3500, 'Within Plate Lavas', fontsize=15)
    ax.set_ylabel("$Ti(ppm)$", fontsize=30)
    ax.set_xlabel("$Zr(ppm)$", fontsize=30)
    ax.set_yscale("log")
    ax.set_xscale("log")
    ax.set_aspect(0.8)
    ax.set_xlim((10, 1000))
    ax.set_ylim((1000, 40000))
    return PearceDiscrimin, ax
def plotPierce(data, save=False, nombre = 'Pierce'):
    muestras = data.index
    loscolores=["lawngreen", "cyan", "gold", "fuchsia", "r", "indigo"]
    Zrppm = data['Zr']
    TiO2 = data['TiO2']
    mTi = 47.86
    mO = 16.
    Tippm = TiO2*1e4*mTi/(2*mO+mTi)
    PearceDiscrimin, ax=buildPierce()
    ax.scatter(Zrppm, Tippm, c=loscolores, s=100)
    for i, txt in enumerate(muestras):
        ax.annotate(txt, (Zrppm[i]-20,Tippm[i]-100))
    if save:
        plt.tight_layout()
        plt.gcf()
        plt.savefig(nombre+'.png', dpi=300)
