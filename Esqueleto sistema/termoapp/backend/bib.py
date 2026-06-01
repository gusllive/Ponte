import numpy as np
import pandas as pd
from scipy import integrate
from scipy.optimize import root

def f_n_param(vp):
  # Normalizacao dos parametros da eq. cubica
  #  de forma que a = 1
  vp_n = vp/vp[0]
  return vp_n

def f_raizes_cubica(vp):
  # Calculo e critica das raizes de uma cubica
  #  Fornece somente as raízes reais!
  vp_n = f_n_param(vp)
  a = vp_n[2-1]
  b = vp_n[3-1]
  c = vp_n[4-1]
  Q = (a**2 - 3*b)/9
  R = (2*a**3 - 9*a*b + 27*c)/54
  M = R**2 - Q**3
  if (M < 0):
    tetha = np.arccos(R/np.sqrt(Q**3))
    arg   = np.zeros((3,))
    x     = np.zeros((3,))
    arg[1-1] = tetha/3
    arg[2-1] = (tetha + 2*np.pi)/3
    arg[3-1] = (tetha - 2*np.pi)/3
    x[1-1] = -(2*np.sqrt(Q)*np.cos(arg[1-1])) - a/3
    x[2-1] = -(2*np.sqrt(Q)*np.cos(arg[2-1])) - a/3
    x[3-1] = -(2*np.sqrt(Q)*np.cos(arg[3-1])) - a/3
  else:
    S = -np.sign(R)*(abs(R) + np.sqrt(M))**(1/3)
    if(S != 0):
      TT = Q/S
    else:
      TT = 0
    x = S + TT - (a/3)
  return {'x': x, 'discriminante': M}

def f_cubica(x,vp):
  # Funcao cubica - polinomio de 3o grau
  a1 = vp[1-1]
  b1 = vp[2-1]
  c1 = vp[3-1]
  d1 = vp[4-1]
  y = a1*x**3 + b1*x**2 + c1*x + d1
  return y

def f_error(x, a, b):
  z = 0.0
  nt = len(b)
  for i in range(0,nt):
    z = z + a[i] * x**(b[i])
  return z

def allroots_fat(a, b):
  # a -> parametros do polinomio
  # b -> graus dos termos monomiais
  #      ex: cubica b = np.array([3,2,1,0])
  a1 = a
  b1 = b
  n = len(b) - 1
  a = a/a[1-1]
  # matrix(0, ncol = n, nrow = n)
  b = np.zeros((n,n))
  for i in range(0,n-1):
    #print(n,i)
    b[i, i + 1] = 1.0
  for i in range(0,n):
    #print(n,i)
    b[n-1, i] = -a[n-1 + 2 - i-1]
  c = np.linalg.eigvals(b)
  # (list(x = c$values, error = f_error(c$values, a1, b1)))
  return {'x': c, 'f_error': f_error(c, a1, b1)}

def f_conv_param(param):
    # Parametros da Eq. 3.52 para Z
    # Z = fator de compressibilidade
    beta_f     = param[0]
    q_f        = param[1]
    epsilon_f = param[2]
    sigma_f    = param[3]
    # Parametros da cubica:
    # a * x**3 + b * x**2 + c * x + d = 0
    a = 1
    b = beta_f*sigma_f + beta_f*epsilon_f - beta_f - 1
    c = ((beta_f**2*epsilon_f - beta_f**2 - beta_f)*sigma_f +
          beta_f*q_f + (-beta_f**2 - beta_f)*epsilon_f)
    d = epsilon_f*sigma_f*(-beta_f**3 - beta_f**2) - (beta_f**2 * q_f)
    #
    param_novo = [a, b, c, d]
    #param_novo = dict(zip(['a', 'b', 'c', 'd'], param_novo))
    param_novo = np.array([a,b,c,d])
    return param_novo

def f_interp_F1(x0,x,y):
  # Verificando
  if ((x0 < x[0]) | (x0 > x[1])):
    return print('x0 fora da faixa!')
  # Interpolacao linear em uma direcao
  y0 = ((x[1] - x0)/(x[1] - x[0]))*y[0] + ((x0   - x[0])/(x[1] - x[0]))*y[1]
  return float(y0)

def f_interp_F2(x0,x,y1,y2,z0,z):
  # Verificando
  if ((x0 < x[0]) | (x0 > x[1])):
    return print('x0 fora da faixa!')
  if ((z0 < z[0]) | (z0 > z[1])):
    return print('z0 fora da faixa!')
  # Interpolacao em duas direcoes
  z1 = f_interp_F1(x0,x,y1)
  z2 = f_interp_F1(x0,x,y2)
  #zz = f_interp_F1(z0,z,np.array([z1,z2]))
  zz = f_interp_F1(z0,z,(z1,z2))
  return zz

def f_CpsR(T1, param):
  # eq.4.4 - p.94 - SVNA
  # Fornece Cp / R - adimensional
  A = param[0]
  B = param[1]
  C = param[2]
  D = param[3]
  CpsR = A + B*T1 + C*T1**2 + D*T1**(-2)
  return CpsR

def f_cp_vap_db(Temp,param):
    '''Função que calcula cp do vapor como  gás ideal para os dados do 
        databank_properties.pickle
    '''
    a = param[0]
    b = param[1]
    c = param[2]
    d = param[3]
    #
    cp = a + b*Temp + c*Temp**2 + d*Temp**3
    # attr(x = cp, which = "units") = "cal/mol_K"
    cp = 4.184 * cp # conversão de cal para J (Joules)
    #cp = 1000.0 * cp # conversão de mol para kmol
    return cp # J/mol/K

def f_cp_param_db(T1, lista_componentes, dados):
    '''Função que monta uma matriz com os parâmetros de todos os compoenente da 
        lista_componentes e também calcula o valor de cp de cada um deles na 
        temperatura T1
        Entradas:
        T1 = temperatura em K
        lista_componentes =
        dados =
        Saidas:
        v_cp = vetor com os valores de cp @T1 em cal/mol/K
        M_param = matriz com os quatro parâmetrso da equação do modelo de cp, sendo um
                  componente por linha na mesma ordem de lista_componentes
        '''
    nc = len(lista_componentes)
    M_param = np.empty((nc,4))
    v_cp = np.empty((nc))
    k = 0
    for i_num in lista_componentes:
        #print(i_num)
        param = dados [dados['num'] == i_num][['cp_a', 'cp_b', 'cp_c', 'cp_d']]
        param = param.to_numpy()[0]
        M_param[k,:] = param
        v_cp[k] = f_cp_vap_db(T1,param)
        k += 1
    # v_cp em J/mol/K
    return (v_cp, M_param)

def f_ICPH(T1, T2, iteq, A, B = 0, C = 0, D = 0):
  ''' Fornece a integral de Cp/R ou de cP (databank)
      Temperatura em K - eq.4.7 p.97 do SVNA
      Entradas:
      T1: temperatutar inicial ou temperatura de referência em K
      T2: temperatura final em K
      iteq: índice do tipo da equação que será utilizada
            1 - equação CpsR do SVNA
            2 - equaçáo de cp do databamk
      A: parâmetro A ou somente o vetor com os parâmetros
      B: parâmetro B
      C: parâmetro C
      D: parâmetro D
      Saídas:
      DH: delta H entre T1 e T2 em J/mol que é igual a kJ/kmol
  '''
  R_ig = 8.314 # J/(mol.K)
  npv  = 4
  if ((type(A) == list)|(type(A) == np.ndarray)):
    param = A
    A = param[1-1]
    B = param[2-1]
    C = param[3-1]
    D = param[4-1]
  else:
    param = np.zeros((npv,))
    param[1-1] = A
    param[2-1] = B
    param[3-1] = C
    param[4-1] = D
  #
  i_CpsR = 0.0
  DH     = 0.0
  if (iteq == 1):
    i_CpsR = integrate.quad(f_CpsR, T1, T2, args=(param,))[0]
    DH     = i_CpsR*R_ig
  elif (iteq == 2):
    DH     = integrate.quad(f_cp_vap_db, T1, T2, args=(param,))[0]
    i_CpsR = DH/R_ig
  #
  return {'i_CpsR': i_CpsR, 'DH': DH}

def f_dT(x):
  y = 1.0
  return y

def f_MCPH(T1,T2, iteq, param):
  # Fornece o Cp/R medio na faixa de temperatura
  #  entre T1 e T2 - p.98 do SVNA
  # #  eq.4.8
  R_ig = 8.314 # J/(mol.K)
  deno = integrate.quad(f_dT, T1, T2)[0]
  CpsR_medio = 0.0
  if(iteq == 1):
      nume = integrate.quad(f_CpsR, T1, T2, args=(param,))[0]
      CpsR_medio = nume / deno
  elif(iteq == 2):
      nume = integrate.quad(f_cp_vap_db, T1, T2, args=(param,))[0]
      CpsR_medio = nume / deno / R_ig
  return CpsR_medio

def f_1sTdT(x):
  y = 1.0 / x
  return y

def f_CpsRsT (Temp, iteq, param):
  '''Retorna o valor de Cp/(R * T)
       OBS: parte da eq.5.14 p.127
       Temp em K 
  '''
  CpsRsT = 0.0
  if(iteq == 1):
    CpsRsT = f_CpsR(Temp, param) / Temp
  elif(iteq == 2):
    R_ig = 8.314 # J/(mol.K)
    CpsRsT = f_cp_vap_db(Temp,param) / R_ig / Temp
  # CpsR = cp / R ,adimensional
  return CpsRsT

def f_ICPS(T1, T2, iteq, A, B = 0, C = 0, D = 0):
  ''' Fornece a integral de Cp/R ou de cP (databank)
      Temperatura em K - eq.5.15 p.127 do SVNA
      Entradas:
      T1: temperatutar inicial ou temperatura de referência em K
      T2: temperatura final em K
      iteq: índice do tipo da equação que será utilizada
            1 - equação CpsR do SVNA
            2 - equaçáo de cp do databamk
      A: parâmetro A ou somente o vetor com os parâmetros
      B: parâmetro B
      C: parâmetro C
      D: parâmetro D
      Saídas:
      DH: delta H entre T1 e T2 em J/mol que é igual a kJ/kmol
  '''
  R_ig = 8.314 # J/(mol.K)
  npv = 4
  if ((type(A) == list)|(type(A) == np.ndarray)):
    param = A
    A = param[1-1]
    B = param[2-1]
    C = param[3-1]
    D = param[4-1]
  else:
    param = np.zeros((npv,))
    param[1-1] = A
    param[2-1] = B
    param[3-1] = C
    param[4-1] = D
  #
  i_CpsRsT = integrate.quad(f_CpsRsT, T1, T2, args=(iteq, param))[0]
  DS = i_CpsRsT*R_ig
  #
  return {'i_CpsRsT': i_CpsRsT, 'DS': DS}

def f_MCPS(T1,T2, iteq, param):
  # Fornece o Cp/R/T médio na faixa de temperatura
  #  entre T1 e T2 - p.128 do SVNA
  #  eq.5.17 p.128
  # R_ig = 8.314 # J/(mol.K)
  deno = integrate.quad(f_1sTdT, T1, T2)[0]
  nume = integrate.quad(f_CpsRsT, T1, T2, args=(iteq,param))[0]
  CpsRsT_medio = nume / deno
  return CpsRsT_medio

def f_HRB(Tr,Pr,omega):
  # Entalpia residual pela abordagem dos estados correspondentes
  # eq.6.87 - p.174
  B0 = 0.083 - (0.422 / Tr**1.6)
  dB0dTr = 0.675 / (Tr**2.6)
  B1 = 0.139 - (0.172 / Tr**4.2)
  dB1dTr = 0.722 / (Tr**5.2)
  parc1 = B0 - Tr*dB0dTr
  parc2 = B1 - Tr*dB1dTr
  Hres_sRsTc = Pr*(parc1 + omega * parc2)
  return Hres_sRsTc

def f_SRB(Tr,Pr,omega):
  # Entropia residual pela abordagem dos estados correspondentes
  # eq.6.88 p.174
  dB0dTr = 0.675 / (Tr**2.6)
  dB1dTr = 0.722 / (Tr**5.2)
  parc1 = dB0dTr
  parc2 = dB1dTr
  Sres_sRsT = -Pr*(parc1 + omega * parc2)
  return Sres_sRsT

def f_P_vap_Clapeyron(T1, A, B):
  # eq.6.75 - p.166 SVNA
  P_vap = np.exp(A + B/T1)
  return P_vap

def f_P_vap_Antoine(T1, param):
  # T1 em K ou °C
  # eq.6.76 - p.166 SVNA
  # param = as.numeric(param)
  a = param[1-1]
  b = param[2-1]
  c = param[3-1]
  #
  Pvap = np.exp(a - (b/(T1 + c)))
  # attr(x = Pvap, which = "units") = "mmHg"
  # Se forem utilizados os parâmetros da Tabela B.2 - p.510 SVNA
  #   a P_vap sera fornecida em kPa
  return Pvap

def f_B0(Tr):
  # eq.3.65 - p.76 SVNA
  f = 0.083 - 0.422 / ((Tr)**1.6)
  return f

def f_B1(Tr):
  # eq.3.66 - p.76 SVNA
  f = 0.139 - 0.172 / ((Tr)**4.2)
  return f

def f_C0(Tr):
  # eq.3.70 - p.77 SVNA
  f = 0.01407 + 0.02432/Tr - 0.00313/(Tr**10.5)
  return f

def f_C1(Tr):
  # eq.3.71 - p.78 SVNA
  f = - 0.02676 + 0.05539/(Tr**2.7) - 0.00242/(Tr**10.5)
  return f

def f_Z_Pitzer_2c(Tr, Pr, omega):
  ''' Fator de compressibilidade cálculado pela correlação de Pitzer
        usando o segundo coeficiente de virial
        Utilizando as equações: 3.57, 3.64, 3.65 e 3.66
  '''
  B0 = f_B0(Tr)
  B1 = f_B1(Tr)
  Z0 = 1 + B0 * Pr/Tr
  Z1 = B1 * Pr/Tr
  Z = Z0 + omega * Z1
  return {'Z': Z, 'Z0': Z0, 'Z1': Z1}

def f_Z_Lee_Kesler_auto(T_r, P_r, omega, path):
    ''' Le as tabelas de dados do Apêndice E do SVNA para os valores de Z0 e Z1.
        Calcula o valor de Z a partir dos dados tabelados das correlações de 
          Lee&Kesler.
        Contribuição de Alcides Temido
        Entradas:
          T_r: temperatura reduzida
          P_r: Pressão reduzida
          omega: fator acêntrico
          path: caminho para a pasta na qual estão os arquivos *.pickle com as tabelas
        Saídas:
          Z_lk: fator acêntrico calculado com os valores das correlações de Lee&Kesler
    '''
    # Leitura das tabelas
    Z0_dados = pd.read_pickle(path + 'Z_Lee_Kesler_Z0_dados.pickle')
    Z1_dados = pd.read_pickle(path + 'Z_Lee_Kesler_Z1_dados.pickle')
    Pr_dados = pd.read_pickle(path + 'Z_Lee_Kesler_Pr_dados.pickle')
    # Localização de T_r
    v_Pr = Pr_dados['Pr'].to_numpy()
    v_Tr = Z0_dados['Tr'].to_numpy()
    i    = np.searchsorted(v_Tr, T_r, 'left')
    x0   = T_r
    x    = (v_Tr[i-1], v_Tr[i])
    # Localização de P_r
    j    = np.searchsorted(v_Pr, P_r, 'left')
    z0   = P_r
    z    = (v_Pr[j-1], v_Pr[j])
    # Interpolação de Z0
    y1_0 = (Z0_dados.loc[i-1].to_numpy()[j-1], Z0_dados.loc[i].to_numpy()[j-1])
    y2_0 = (Z0_dados.loc[i-1].to_numpy()[  j], Z0_dados.loc[i].to_numpy()[  j])
    Z_0  = f_interp_F2(x0,x,y1_0,y2_0,z0,z)
    # Interpolação de Z1
    y1_1 = (Z1_dados.loc[i-1].to_numpy()[j-1], Z1_dados.loc[i].to_numpy()[j-1])
    y2_1 = (Z1_dados.loc[i-1].to_numpy()[  j], Z1_dados.loc[i].to_numpy()[  j])
    Z_1  = f_interp_F2(x0,x,y1_1,y2_1,z0,z)
    # Cálculo de Z_lk
    Z_lk = Z_0 + omega*Z_1
    return {'Z': Z_lk, 'Z0': Z_0, 'Z1': Z_1}

def f_alpha_PR(Tr, omega):
    ''' Tabela 3.1 p.72 do SVNA
    '''
    alpha = ( 1.0 + (0.37464 + 1.54226*omega -\
                   0.26992*omega**2)*\
           (1.0 - np.sqrt(Tr)))**2
    return alpha

def f_residuo_Z_3_52(Z, param):
    ''' Eq. 3.52 p.72 do SVNA escrita na forma de resíduo (igualada a zero)'''
    beta     = param[0]
    q        = param[1]
    episilon = param[2]
    sigma    = param[3]
    #
    fat = (Z-beta)/(Z+episilon*beta)/(Z+sigma*beta)
    res = 1.0 + beta - q*beta*fat - Z
    return res

def f_a_eq_3_45(Tr, omega, Psi, R_ig, Tc, Pc):
    ''' Valor de a(T) para ser utilizado nas eq. 3.49 e 3.55, calculado segundo
          a eq. 3.45 da p.69
    '''
    alpha = f_alpha_PR(Tr, omega)
    a = Psi*alpha*R_ig**2*Tc**2/Pc
    return a 

def f_b_eq_3_46(Omega, R_ig, Tc, Pc):
    ''' Valor de b para ser utilizado nas eq. 3.49 e 3.55, calculado segundo
          a eq. 3.46 da p.70
    '''
    b = Omega*R_ig*Tc/Pc
    return b

def f_residuo_V_3_49(V, T, P, param, Omega, Psi, R_ig, omega, Tc, Pc):
    ''' Eq. 3.49 p.71 do SVNA escrita na forma de resíduo (igualada a zero)
    '''
    #beta     = param[0]
    #q        = param[1]
    episilon = param[2]
    sigma    = param[3]
    #
    Tr = T/Tc
    b  = f_b_eq_3_46(Omega, R_ig, Tc, Pc)
    a  = f_a_eq_3_45(Tr, omega, Psi, R_ig, Tc, Pc)
    #
    fat = (V-b)/(V + episilon*b)/(V + sigma*b)
    res = R_ig*T/P + b - (a/P)*fat - V
    return res

def f_residuo_Z_3_56(Z, param):
    '''Eq. 3.56 para as raizes de liquidos escrita na forma de resíduo
         (igualada a zero)
    '''
    beta_p    = param[1-1]
    q_p       = param[2-1]
    epsilon_p = param[3-1]
    sigma_p   = param[4-1]
    #
    f1  = Z + epsilon_p * beta_p
    f2  = Z + sigma_p   * beta_p
    f3  = (1.0 + beta_p - Z)/(q_p * beta_p)
    res = Z - (beta_p + (f1*f2*f3))
    return res


def f_flash_RR_fv_residuo(fv, z, K):
    ''' Equação de Rachford-Rice eq.10.17 p.274 SVNA
      Entradas:
        z: composicao da alimentacao, vetor de nc componentes
        K: constante de volatilidade @ T e P dos compoentes, vetor de
           nc componentes
      Saida:
        res: resíduo da equação igualada a zero
    '''
    soma = 0.0
    nc = len(z)
    for i in range(1-1,nc):
        num = z[i]*K[i]
        den = 1.0 + fv*(K[i] - 1.0)
        soma = soma + num/den
    res = soma - 1.0
    return(res)


def f_param_EOS_generalizada(i_EOS,Temp,P,Tc,Pc,omega, R_ig):
    ''' Baseada na Tabela 3.1 p.72 do SVA
        i_EOS - indice da EOS que sera utilizada:
          1 - vdW
          2 - RK
          3 - SRK
          4 - PR
    '''
    #
    Tr = Temp/Tc
    Pr = P/Pc
    #
    alpha   = 0.0
    sigma   = 0.0
    epsilon = 0.0
    Omega   = 0.0
    Psi     = 0.0
    #
    if (i_EOS == 1):
        alpha   = 1.0
        sigma   = 0.0
        epsilon = 0.0
        Omega   = 1/8
        Psi     = 27/64
    elif (i_EOS == 2):
        alpha   = Tr**(-1/2)
        sigma   = 1.0
        epsilon = 0.0
        Omega   = 0.08664
        Psi     = 0.42748
    elif (i_EOS == 3):
        alpha   = (1.0 + (0.480 + 1.574*omega - 0.176*omega**2)*(1 - np.sqrt(Tr)))**2
        sigma   = 1.0
        epsilon = 0.0
        Omega   = 0.08664
        Psi     = 0.42748
    elif (i_EOS == 4):
        alpha   = (1.0 + (0.37464 + 1.54226*omega - 0.26992*omega**2)*(1 - np.sqrt(Tr)))**2
        sigma   = 1.0 + np.sqrt(2)
        epsilon = 1.0 - np.sqrt(2)
        Omega   = 0.07780
        Psi     = 0.45724
    #
    beta = Omega * Pr / Tr        # eq_3_53
    q    = (Psi*alpha)/(Omega*Tr) # eq_3_54
    #
    a = f_a_eq_3_45(Tr, omega, Psi, R_ig, Tc, Pc)
    b = f_b_eq_3_46(Omega, R_ig, Tc, Pc)
    #
    #p_EOS = c(beta,q,epsilon,sigma)
    p_EOS = np.array([beta, q, epsilon, sigma])
    nomes_p_EOS = ("beta","q","epsilon","sigma")
    return {'p_EOS': p_EOS, 'Psi': Psi, 'Omega': Omega, 'a': a, 'b': b,
            'beta': beta, 'q': q, 'epsilon': epsilon, 'sigma': sigma,
            'alpha': alpha, 'Tr': Tr, 'Pr': Pr, 'nomes_p_EOS': nomes_p_EOS}


def f_phi_B(Tr,Pr,omega):
    ''' Calculo de phi com a eq_11_68 p.305 '''
    B0 = f_B0(Tr)
    B1 = f_B1(Tr)
    phi = np.exp((Pr/Tr)*(B0 + omega*B1))
    return phi


def f_PHIB(Tr,Pr,omega):
    ''' Calculo de phi com a eq_11_68 p.305 '''
    B0 = f_B0(Tr)
    B1 = f_B1(Tr)
    phi = np.exp((Pr/Tr)*(B0 + omega*B1))
    return phi


def f_deriv(fun, x, delta, *args):
    ''' Calcula a derivada numérica da função fun no ponto x a 
          partir da perturbação delta em torno do ponto x  '''
    y1 = fun(x - delta, *args)
    y2 = fun(x + delta, *args)
    der = (y2 - y1)/(2.0*delta)
    return der

def f_int_I(Z,param):
    ''' Integral da p.163 equivalente as eq. 6_65a e 6_65b
    '''
    beta_f     = param[1-1]
    q_f        = param[2-1]
    epsilon_f  = param[3-1]
    sigma_f    = param[4-1]
    #
    int_I = 0.0
    if (epsilon_f != sigma_f):
        fat = np.log((Z + sigma_f*beta_f) / (Z + epsilon_f*beta_f))
        int_I = (1.0/(sigma_f - epsilon_f))*fat
    else:
        int_I = beta_f/(Z + epsilon_f*beta_f)
    return int_I

def f_alpha_EOS(Tr, i_EOS, omega):
    ''' alpha(Tr) da EOS segundo a Tabela 3.1 p.72 '''
    alpha = 0.0
    if (i_EOS == 1):
        alpha = 1.0
    elif (i_EOS == 2):
        alpha = Tr**(-1/2)
    if (i_EOS == 3):
        alpha = (1.0 + (0.480 + 1.574*omega - 0.176*omega**2)*(1 - np.sqrt(Tr)))**2
    if (i_EOS == 4):
        alpha = (1.0 + (0.37464 + 1.54226*omega - 0.26992*omega**2)*(1 - np.sqrt(Tr)))**2
    return alpha


def f_q_3_54(Tr,i_EOS, omega):
    Psi   = 0.0
    Omega = 0.0
    if (i_EOS == 1):
        Omega = 1/8
        Psi   = 27/64
    elif (i_EOS == 2):
        Omega = 0.08664
        Psi   = 0.42748
    elif (i_EOS == 3):
        Omega = 0.08664
        Psi   = 0.42748
    elif (i_EOS == 4):
        Omega = 0.07780
        Psi   = 0.45724
    fun = Psi * f_alpha_EOS(Tr, i_EOS,omega) / (Omega * Tr)
    return fun


def f_HR_EOS_eq_6_67(Z, Temp, Tc, i_EOS, param, omega):
    valor_I = f_int_I(Z, param)
    Tr      = Temp/Tc
    dqdTr   = f_deriv(f_q_3_54,Tr,0.0001, i_EOS, omega)
    R_ig    = 8.314 # J/mol
    H_R     = R_ig*Temp*(Z - 1 + Tr * dqdTr * valor_I)
    # H_R # J/mol
    #
    H_RsRsT = H_R/(R_ig*Temp)
    #
    return {'H_R': H_R, 'H_RsRsT': H_RsRsT}


def f_SR_EOS_eq_6_68(Z, Temp, Tc, i_EOS, param, omega):
    valor_I = f_int_I(Z, param)
    Tr      = Temp/Tc
    dqdTr   = f_deriv(f_q_3_54,Tr,0.0001, i_EOS, omega)
    R_ig    = 8.314 # J/mol
    beta_p  = param[1-1]
    q_p     = param[2-1]
    S_R     = R_ig*(np.log(Z - beta_p) + (q_p + Tr * dqdTr)*valor_I)
    # S_R # J/(mol.K)
    S_RsR = S_R/(R_ig)
    #
    return {'S_R': S_R, 'S_RsR': S_RsR}


def f_deriv_log(fun, x, delta, *args):
    ''' Calcula a derivada numerica da função fun no ponto x a 
          partir da perturbação delta em torno do ponto x
          Contribuição: Clarice Tavares
    '''
    y1 = fun(x - delta, *args)
    y2 = fun(x + delta, *args)
    der = (y2 - y1)/np.log(2.0*delta)
    return der


def f_eq_Harlacher(Pvap, param):
    ''' Equação na forma de resíduo para o cálculo da pressão de vapor utilizando
          o modelo de Harlacher'''
    # param = as.numeric(par_Pvap)
    Temp = param[1-1]
    a    = param[2-1]
    b    = param[3-1]
    c    = param[4-1]
    d    = param[5-1]
    #
    res  = np.log(Pvap) - a - b/Temp - c*np.log(Temp) - (d*Pvap/Temp**2)
    return res


def f_P_vap_Harlacher(Temp, Pvap_guest, param):
    ''' Cálculo a pressão de vapor em mmHg na temperatura Temp '''
    par_lis  = list(param)
    par_Pvap = [Temp] + par_lis
    Pvap =  root(f_eq_Harlacher, Pvap_guest, args=(par_Pvap,)).x[0]
    # attr(x = Pvap, which = "units") = "mmHg"
    return Pvap 


def f_P_vap_Wagner(Temp,CW,Tc,Pc):
    ''' Modelo de P_vap de Wagner'''
    #nc = dim(CW)[1]
    tau   = Temp / Tc
    umtau = 1.0 - tau
    # if (is.array(CW)) {
    # p1 = CW[,1]*umtau
    # p2 = CW[,2]*(umtau)**(1.5)
    # p3 = CW[,3]*(umtau)**(3.0)
    # p4 = CW[,4]*(umtau)**(6.0)
    # } else {
    p1 = CW[1-1]*umtau
    p2 = CW[2-1]*(umtau)**(1.5)
    p3 = CW[3-1]*(umtau)**(3.0)
    p4 = CW[4-1]*(umtau)**(6.0)
    #
    soma = p1 + p2 + p3 + p4
    Pvap = Pc * np.exp((1/tau)*soma)
    return Pvap


def f_phi_Lee_Kesler_auto(Tr, Pr, omega, path):
    ''' Cálculo do coeficiente de fugacidade a partir dos dados da 
          correlação de Lee & Kesler.
          Contribuição de Clarice Tavares
    '''
    # Leitura das tabelas de dados
    phi0_dados = pd.read_pickle(path + 'phi_Lee_Kesler_phi0_dados.pickle')
    phi1_dados = pd.read_pickle(path + 'phi_Lee_Kesler_phi1_dados.pickle')
    Pr_dados   = pd.read_pickle(path + 'phi_Lee_Kesler_v_Pr_dados.pickle')
    Tr_dados   = pd.read_pickle(path + 'phi_Lee_Kesler_v_Tr_dados.pickle')
    #
    v_Pr = Pr_dados['Pr'].to_numpy()
    v_Tr = Tr_dados['Tr'].to_numpy()
    #
    # Localização de T_r
    i    = np.searchsorted(v_Tr, Tr, 'left')
    x0   = Tr
    x    = (v_Tr[i-1], v_Tr[i])
    # Localização de P_r
    j    = np.searchsorted(v_Pr, Pr, 'left')
    z0   = Pr
    z    = (v_Pr[j-1], v_Pr[j])
    #
    # Interpolação de phi0
    y1_0 = (phi0_dados.loc[i-1].to_numpy()[j-1], phi0_dados.loc[i].to_numpy()[j-1])
    y2_0 = (phi0_dados.loc[i-1].to_numpy()[  j], phi0_dados.loc[i].to_numpy()[  j])
    phi0  = f_interp_F2(x0,x,y1_0,y2_0,z0,z)
    # Interpolação de Z1
    y1_1 = (phi1_dados.loc[i-1].to_numpy()[j-1], phi1_dados.loc[i].to_numpy()[j-1])
    y2_1 = (phi1_dados.loc[i-1].to_numpy()[  j], phi1_dados.loc[i].to_numpy()[  j])
    phi1  = f_interp_F2(x0,x,y1_1,y2_1,z0,z)
    # Cálculo de phi_lk
    # Eq. 11.67 p.304
    phi_lk = phi0 * (phi1**omega)
    return {'phi': phi_lk, 'phi0': phi0, 'phi1': phi1}


def f_phi_mist_eq_11_63(y, T, P, Tc_comp, Pc_comp, Vc_comp, Zc_comp, om_comp, k_pib, R_ig):
    nc = Tc_comp.shape[0]
    Tc_mist = np.zeros((nc,nc))
    Pc_mist = np.zeros((nc,nc))
    Vc_mist = np.zeros((nc,nc))
    Zc_mist = np.zeros((nc,nc))
    om_mist = np.zeros((nc,nc))
    #
    for i in range(0,nc):
        for j in range(0,nc):
            #print(i,j)
            if (i == j):
                Tc_mist[i,j] = Tc_comp[i]
                Pc_mist[i,j] = Pc_comp[i]
                Vc_mist[i,j] = Vc_comp[i]
                Zc_mist[i,j] = Zc_comp[i]
                om_mist[i,j] = om_comp[i]
            else:
                # Eq. 11.71
                Tc_mist[i,j] = np.sqrt(Tc_comp[i]*Tc_comp[j])*(1.0 - k_pib[i,j])
                # Eq. 11.74
                Vc_mist[i,j] = ((Vc_comp[i]**(1/3) + Vc_comp[j]**(1/3))/2.0)**3
                # Eq. 11.73
                Zc_mist[i,j] = (Zc_comp[i] + Zc_comp[j])/2.0
                # Eq. 11.72
                Pc_mist[i,j] = (Zc_mist[i,j]*R_ig*Tc_mist[i,j])/Vc_mist[i,j]
                # Eq. 11.70
                om_mist[i,j] = (om_comp[i] + om_comp[j])/2.0
    #
    Tr_mist = np.zeros((nc,nc))
    Pr_mist = np.zeros((nc,nc))
    for i in range(0,nc):
        for j in range(0,nc):
            Tr_mist[i,j] = T / Tc_mist[i,j]
            Pr_mist[i,j] = P / Pc_mist[i,j]
    #
    B0_mist = np.zeros((nc,nc))
    B1_mist = np.zeros((nc,nc))
    # B chapeu da mistura
    Bc_mist = np.zeros((nc,nc))
    B_mist = np.zeros((nc,nc))
    for i in range(0,nc):
        for j in range(0,nc):
            B0_mist[i,j] = f_B0(Tr_mist[i,j])
            B1_mist[i,j] = f_B1(Tr_mist[i,j])
            # Eq. 11.69a
            Bc_mist[i,j] = B0_mist[i,j] + om_mist[i,j]*B1_mist[i,j]
            # Eq. 11.69b
            B_mist[i,j]  = Bc_mist[i,j]*R_ig*Tc_mist[i,j]/Pc_mist[i,j]
    #
    delta_mist = np.zeros((nc,nc))
    for i in range(0,nc):
        for j in range(0,nc):
            delta_mist[i,j] = 2.0*B_mist[i,j] - B_mist[i,i] - B_mist[j,j]
    #
    phi = np.zeros((nc,))
    for k in range(0,nc):
        soma = 0.0
        for i in range(0,nc):
            for j in range(0,nc):
                soma = soma + y[i]*y[j]*(2.0*delta_mist[i,k] + delta_mist[i,k])
        fat = B_mist[k,k] + (1.0/2.0)*soma
        # Eq. 11.64
        phi[k] = np.exp((P*fat)/(R_ig*T))
    return {'phi': phi, 'B_chapeu': Bc_mist, 'B_mist': B_mist}


def f_phi_EOS_eq_11_37(Z, param):
    I = f_int_I(Z, param)
    # Cálculo de phi com a eq_11_37 p.296
    beta = param[1-1]
    q    = param[2-1]
    #
    phi_EOS = np.exp(Z - 1 - np.log(Z - beta) - q*I)
    #
    return phi_EOS


def f_DHvap_Riedel_eq_4_12(T_eb, Tc, Pc, R_ig):
    '''  Cálculo do DH_vap de uma substância no ponto de ebulição a partir
           das proppriedades críticas - Modelo de Riedel Eq. 4.12 p.100 do SVNA
    '''
    Tr_eb  = T_eb / Tc
    fat    = np.log(Pc) - 1.013
    num    = R_ig*T_eb*1.092*fat
    den    = 0.93 - Tr_eb
    DH_vap = num/den
    #
    return DH_vap


def f_DHvap_Watson(T1, DHvap1, T2, Tc):
    ''' A partir de um valor de DH_vap_1 a uma T_1, calcula o DH_vap_2 na temperatura T2 dada.
          Modelo de Watson Eq. 4.13 na p.100 do SVNA 
    '''
    Tr1    = T1/Tc
    Tr2    = T2/Tc
    DHvap2 = DHvap1*((1.0 - Tr2)/(1.0 - Tr1))**0.38
    #
    return DHvap2


def f_B_chapeu_dependente_T(T1,Tc,Pc,Vc,Zc,omega,k):
  # B da Eq. na forma Virial
  # para nc = 2 (dois componentes na mistura)
  # (T1,P,y,Tc,Pc,Vc,Zc,omega,k)
  # P em bar
  # T em K
  # V em cm3
  #
  # k = matrix(0,nrow = 2, ncol = 2)
  #
  # equacao 11.70
  R = 8314.00 # cm3 KPa/ (K mol)
  nc = len(Tc)
  omega_12 = np.mean(omega)
  omega_m = np.array([[omega[1-1], omega_12], 
                      [omega_12, omega[2-1]]])
  #omega_m = matrix(omega_m,nrow = nc, ncol = nc)
  # equacao 11.71
  Tc_12 = np.sqrt(Tc[1-1]*Tc[2-1])*(1 - k[1-1,2-1])
  # equacao 11.73
  Zc_12 = np.mean(Zc)
  # equacao 11.74
  Vc_12 = (np.mean(Vc**(1/3)))**3
  # equacao 11.72
  Pc_12 = R * Zc_12 * Tc_12 / Vc_12
  #Tr_m = matrix(0,nrow = nc, ncol = nc)
  Tr_m = np.zeros((nc,nc))
  #B0_m = matrix(0,nrow = nc, ncol = nc)
  B0_m = np.zeros((nc,nc))
  #B1_m = matrix(0,nrow = nc, ncol = nc)
  B1_m = np.zeros((nc,nc))
  #
  Tr_m[1-1,1-1] = T1 / Tc[1-1]
  Tr_m[2-1,2-1] = T1 / Tc[2-1]
  Tr_m[1-1,2-1] = T1 / Tc_12
  Tr_m[2-1,1-1] = Tr_m[1-1,2-1]
  #
  B0_m[1-1,1-1] = f_B0(Tr_m[1-1,1-1])
  B0_m[2-1,2-1] = f_B0(Tr_m[2-1,2-1])
  B0_m[1-1,2-1] = f_B0(Tr_m[1-1,2-1])
  B0_m[2-1,1-1] = f_B0(Tr_m[2-1,1-1])
  #
  B1_m[1-1,1-1] = f_B1(Tr_m[1-1,1-1])
  B1_m[2-1,2-1] = f_B1(Tr_m[2-1,2-1])
  B1_m[1-1,2-1] = f_B1(Tr_m[1-1,2-1])
  B1_m[2-1,1-1] = f_B1(Tr_m[2-1,1-1])
  # Combinacao das equacoes 11.69a e 11.69b
  B_chapeu = B0_m + omega_m * B1_m
  #
  Tc_m = np.array([[Tc[1], Tc_12],
                   [Tc_12, Tc[2]]])
  #Tc_m = matrix(Tc_m, nrow = nc, ncol = nc)
  #
  Pc_m = np.array([[Pc[1], Pc_12], 
                   [Pc_12, Pc[2]]])
  #Pc_m = matrix(Pc_m, nrow = nc, ncol = nc)
  #
  #B_m = B_chapeu * R * Tc_m / Pc_m
  return(B_chapeu)

def f_B_mistura(Temp,Tc,Pc,Vc,Zc,omega,k,y):
  # B da Eq.11.61
  # Sistema binários: nc=2
  B_chapeu = f_B_chapeu_dependente_T(Temp,Tc,Pc,Vc,Zc,omega,k)
  B = y[1-1]**2*B_chapeu[1-1,1-1] + 2*y[1-1]*y[2-1]*B_chapeu[1-1,2-1] + y[2-1]**2*B_chapeu[2-1,2-1]
  return(B)

def f_V_R_eq_6_40(Z, T, P, R_ig):
    ''' Calcula o V_R a partir da equação 6.40 da
        p. 155 do SVNA
        Entrada:
          Z: fator de compressibilidade calculado para a fase adequada
          T: temperatura na unidade de T presente em R_ig
          P: pressão na unidade de P presente em R_ig
          R_ig: constante do gás ideal nas unidades desejadas
        Saida:
          V_R: volume específico nas unidades presentes me R_ig
    '''
    #
    V_R = ((R_ig*T)/P)*(Z - 1.0)
    #
    return V_R

def f_G_R_eq_6_66b(Z, T, param_EOS):
    ''' Calcula o G_R a partir da equação 6.66b da p. 165 do SVNA
        Entrada:
          Z: fator de compressibilidade calculado para a fase adequada
          T: temperatura em K
          param_EOS: [beta, q, epsilon, sigma]
        Saida:
          G_R: energia libre de Gibbs residual em J/mol
    '''
    I    = f_int_I(Z, param_EOS)
    q    = param_EOS[1]
    beta = param_EOS[0]
    R_ig = 8.314 # J/mol/K
    #
    G_RsRsT = Z - 1.0 - np.log(Z - beta) - q*I
    G_R = G_RsRsT*R_ig*T
    #
    return {'G_R': G_R, 'G_RsRsT': G_RsRsT}


def f_rho_eq_6_57(Z, T, P, R_ig):
    ''' Calcula rho = 1/ V  - massa molar específica segundo a equação 6.57 da p. 163 do SVNA'''
    rho = P / (Z*R_ig*T)
    #
    return rho


def f_res_Z_3_68(Z, B_chapeu, C_chapeu, P_r, T_r):
    parc1 = (B_chapeu*P_r)/(T_r*Z)
    parc2 = C_chapeu*(P_r/(T_r*Z))**2
    res = Z - (1.0 + parc1 + parc2)
    return res


def f_param_virial_Pitzer(T, P, omega, T_c, P_c, R_ig):
    T_r = T/T_c
    P_r = P/P_c
    #
    B_0 = f_B0(T_r)
    B_1 = f_B1(T_r)
    B_chapeu = B_0 + omega*B_1
    B = R_ig*T_c*B_chapeu/(P_c)
    #
    Z_3_61 = 1.0 + B_chapeu*(P_r/T_r)
    #
    C_0 = f_C0(T_r)
    C_1 = f_C1(T_r)
    C_chapeu = C_0 + omega*C_1
    C = (R_ig**2)*(T_c**2)*C_chapeu/(P_c**2)
    #
    Z_3_68 = root(f_res_Z_3_68, Z_3_61, args=(B_chapeu, C_chapeu, P_r, T_r)).x[0]
    #
    return {'B': B, 'B_chapeu': B_chapeu, 'B_0': B_0, 'B_1': B_1, 'Z_3_61': Z_3_61,
            'C_0': C_0, 'C_1': C_1, 'C_chapeu': C_chapeu, 'C': C, 'Z_3_68': Z_3_68}


def f_G_R_virial_Pitzer_eq_6_61(Z, T, P, omega, T_c, P_c, R_ig):
    ''' Cálculo da energia livre de Gibbs residual de acordo com
          a equação 6.61 p.162 SVNA'''
    #
    rho = f_rho_eq_6_57(Z, T, P, R_ig)
    rpv = f_param_virial_Pitzer(T, P, omega, T_c, P_c, R_ig)
    B = rpv['B']
    C = rpv['C'] 
    #
    GRsRsT = 2.0*B*rho + (3/2)*C*rho**2 - np.log(Z)
    GR = GRsRsT*R_ig*T
    #
    return {'GR': GR, 'GRsRsT': GRsRsT}


def f_dBdT_dCdT(T, P, omega, T_c, P_c, R_ig):
    delta_T = 0.001
    rpv1 = f_param_virial_Pitzer(T - delta_T, P, omega, T_c, P_c, R_ig)
    rpv2 = f_param_virial_Pitzer(T + delta_T, P, omega, T_c, P_c, R_ig)
    #
    B_1 = rpv1['B']
    B_2 = rpv2['B']
    delta_B = B_2 - B_1
    #
    C_1 = rpv1['C']
    C_2 = rpv2['C']
    delta_C = C_2 - C_1
    #
    dBdT = (delta_B/delta_T)
    dCdT = (delta_C/delta_T)
    #
    return {'dBdT': dBdT, 'dCdT': dCdT}


def f_H_R_virial_Pitzer_eq_6_62(Z, T, P, omega, T_c, P_c, R_ig):
    ''' Cálculo da entalpia residual de acordo com a equação 6.62 p.162 SVNA '''
    rho = f_rho_eq_6_57(Z, T, P, R_ig)
    rpv = f_param_virial_Pitzer(T, P, omega, T_c, P_c, R_ig)
    B = rpv['B']
    C = rpv['C']
    #
    r_ddT = f_dBdT_dCdT(T, P, omega, T_c, P_c, R_ig)
    dBdT = r_ddT['dBdT']
    dCdT = r_ddT['dCdT']
    #
    parc1 = ((B/T) - dBdT)*rho
    parc2 = ((C/T) - (1/2)*dCdT)*(rho**2)
    #
    HRsRsT = T*(parc1 + parc2)
    HR     = HRsRsT*R_ig*T
    #
    return {'HR': HR, 'HRsRsT': HRsRsT}


def f_S_R_virial_Pitzer_eq_6_63(Z, T, P, omega, T_c, P_c, R_ig):
    ''' Cálculo da entropia residual de acordo com a equação 6.63 p.162 SVNA '''
    rho = f_rho_eq_6_57(Z, T, P, R_ig)
    rpv = f_param_virial_Pitzer(T, P, omega, T_c, P_c, R_ig)
    B = rpv['B']
    C = rpv['C']
    #
    r_ddT = f_dBdT_dCdT(T, P, omega, T_c, P_c, R_ig)
    dBdT = r_ddT['dBdT']
    dCdT = r_ddT['dCdT']
    #
    parc1 = ((B/T) + dBdT)*rho
    parc2 = (1/2)*((C/T) + dCdT)*(rho**2)
    #
    SRsR = np.log(Z) - T*(parc1 + parc2)
    SR   = SRsR*R_ig
    #
    return {'SR': SR, 'SRsR': SRsR}


def f_der_B_mistura_rel_T(Temp,Tc,Pc,Vc,Zc,omega,k,y,h_der):
    # B da Eq. na forma Virial
    B1  = f_B_mistura(Temp + h_der,Tc,Pc,Vc,Zc,omega,k,y)
    B2  = f_B_mistura(Temp - h_der,Tc,Pc,Vc,Zc,omega,k,y)
    der = (B1 - B2)/(2*h_der)
    return(der)


def f_calc_DH_vap_pela_Pvap(T, P, par_Antoine, T_cf, T_ff, npg, Tc, Pc, omega, i_EOS):
    ''' Calcula a variação da entalpia na vaporização utilizando a informação do modelo
          de P_sat de Antoine e uma equação de estado (EOS)
          Usa a Eq. 6.74 p.165 do SVNA
          Entrada:
            T:           Temperatura em K
            P:           Pressão em bar
            par_Antoine: Valores de A_i, B_i e C_i, segundo a tabela B.2 p.510 do SVNA
            T_cf:        Temperatura em °C do começo da fiaxa de validade mo modelo
            T_ff:        Temperatura em °C do final  da fiaxa de validade mo modelo
            npg:         Quantidade de pontos usados na geração da curva para o cáculo da derivada
            Tc:          Temperatura crítica do componente em K
            Pc:          Pressão crítica em bar
            omega:       Fator acêntrico do componente
            i_EOS:       indice da EOS que sera utilizada:
              1 - vdW
              2 - RK
              3 - SRK
              4 - PR
            Saida:
              DH_vap_01:  Calor de vaporização em J/mol com DZ = 1.0
              P_vap_T:    Pressão de vapor em bar na temperatura T
              DZ_vap_rig: DZ rigoroso calculado com a EOS selecionada
              DH_vap_02:  Calor de vaporização em J/mol com DZ dado pela EOS
    '''
    T_oC = T - 273.15
    P_vap_T = f_P_vap_Antoine(T_oC,par_Antoine)*1000.0 # Pa
    P_vap_T = P_vap_T / 1.0e5 # bar
    if (T_cf == 0.0):
          T_cf = (T_oC - 20.0) + 273.15
          T_ff = (T_oC + 20.0) + 273.15
    T_faixa = np.linspace(T_cf - 273.15, T_ff - 273.15, npg) # °C
    P_sat_faixa = np.zeros((npg,))
    for i in range(0,1000):
          P_sat_faixa[i] = f_P_vap_Antoine(T_faixa[i],par_Antoine)*1000.0 # Pa
    df = pd.DataFrame({'T_oC': T_faixa,'P_sat_Pa': P_sat_faixa})
    df['ln_Psat'] = np.log(df['P_sat_Pa'])
    df['v_1sT'] = 1.0/(df['T_oC'] + 273.15)
    df_dif = df[['ln_Psat', 'v_1sT']].diff()
    df_dif.rename(columns={"ln_Psat": "d_ln_Psat", "v_1sT": 'd_v_1sT'}, inplace=True)
    df = df.join(df_dif)
    # Calculando a derivada correspondente à equação 6.74
    df['dlnPd1sT'] = df['d_ln_Psat']/df['d_v_1sT']
    cond1 = df['T_oC'] > (T_oC - 1.0)
    cond2 = df['T_oC'] < (T_oC + 1.0)
    dlnPd1sT_at_T = df[cond1 & cond2]['dlnPd1sT'].mean()
    # Cálculo com DZ aproximado
    R_ig = 8.314 #J/mol/°C
    DZ_vap_aprox = 1.0
    DH_vap_01 = - dlnPd1sT_at_T * R_ig * DZ_vap_aprox
    # Cálculo com DZ rigoroso
    R_ig = 83.14  # bar*cm3/mol/K
    resp_par_EOS = f_param_EOS_generalizada(i_EOS, T_oC+273.15, P, Tc, Pc, omega, R_ig)
    par_EOS = resp_par_EOS['p_EOS']
    par_cubica = f_conv_param(par_EOS)
    resp_Z = f_raizes_cubica(par_cubica)
    Z_v = np.max(resp_Z['x'])
    Z_l = np.min(resp_Z['x'])
    DZ_vap_rig = Z_v - Z_l
    R_ig = 8.314 #J/mol/°C
    DH_vap_02 = - dlnPd1sT_at_T * R_ig * DZ_vap_rig
    return {'DH_vap_01': DH_vap_01, 'P_vap_T': P_vap_T, 'DZ_vap_rig': DZ_vap_rig,
            'DH_vap_02': DH_vap_02, 'dlnPd1sT_at_T': dlnPd1sT_at_T}


def f_DS_ig_T_P_eq_6_96(T1, T2, P1, P2, iteq, par):
    R_ig = 8.314 # J/(mol.K)
    DS_ig_T = f_ICPS(T1, T2, iteq, par)['DS']
    DS_ig_P = R_ig*np.log(P2/P1)
    DS_ig = DS_ig_T - DS_ig_P
    return {'DS_ig_T': DS_ig_T, 'DS_ig_P': DS_ig_P, 'DS_ig': DS_ig }


def f_calc_DH_vap_pela_Pvap_bar_K(T, P, par_Antoine, T_cf, T_ff, npg, Tc, Pc, omega, i_EOS):
    ''' Calcula a variação da entalpia na vaporização utilizando a informação do modelo
          de P_sat de Antoine e uma equação de estado (EOS)
          Usa a Eq. 6.74 p.165 do SVNA
          Entrada:
            T:           Temperatura em K
            P:           Pressão em bar
            par_Antoine: Valores de A_i, B_i e C_i, para a temperatura em K e a pressão de vapor em bar
            T_cf:        Temperatura em °C do começo da fiaxa de validade mo modelo
            T_ff:        Temperatura em °C do final  da fiaxa de validade mo modelo
            npg:         Quantidade de pontos usados na geração da curva para o cáculo da derivada
            Tc:          Temperatura crítica do componente em K
            Pc:          Pressão crítica em bar
            omega:       Fator acêntrico do componente
            i_EOS:       indice da EOS que sera utilizada:
              1 - vdW
              2 - RK
              3 - SRK
              4 - PR
            Saida:
              DH_vap_01:  Calor de vaporização em J/mol com DZ = 1.0
              P_vap_T:    Pressão de vapor em bar na temperatura T
              DZ_vap_rig: DZ rigoroso calculado com a EOS selecionada
              DH_vap_02:  Calor de vaporização em J/mol com DZ dado pela EOS
    '''
    T_K = T - 273.15
    P_vap_T = f_P_vap_Antoine(T,par_Antoine)*1000.0 # bar
    #P_vap_T = P_vap_T / 1.0e5 # bar
    if (T_cf == 0.0):
          T_cf = (T - 20.0)
          T_ff = (T + 20.0)
    T_faixa = np.linspace(T_cf, T_ff, npg) # K
    P_sat_faixa = np.zeros((npg,))
    for i in range(0,1000):
          P_sat_faixa[i] = f_P_vap_Antoine(T_faixa[i],par_Antoine)*100.0 # Pa
    df = pd.DataFrame({'T_K': T_faixa,'P_sat_Pa': P_sat_faixa})
    df['ln_Psat'] = np.log(df['P_sat_Pa'])
    df['v_1sT'] = 1.0/(df['T_K'])
    df_dif = df[['ln_Psat', 'v_1sT']].diff()
    df_dif.rename(columns={"ln_Psat": "d_ln_Psat", "v_1sT": 'd_v_1sT'}, inplace=True)
    df = df.join(df_dif)
    # Calculando a derivada correspondente à equação 6.74
    df['dlnPd1sT'] = df['d_ln_Psat']/df['d_v_1sT']
    cond1 = df['T_K'] > (T - 1.0)
    cond2 = df['T_K'] < (T + 1.0)
    dlnPd1sT_at_T = df[cond1 & cond2]['dlnPd1sT'].mean()
    # Cálculo com DZ aproximado
    R_ig = 8.314 # J/mol/°C
    DZ_vap_aprox = 1.0
    DH_vap_01 = - dlnPd1sT_at_T * R_ig * DZ_vap_aprox
    # Cálculo com DZ rigoroso
    R_ig = 83.14  # bar*cm3/mol/K
    resp_par_EOS = f_param_EOS_generalizada(i_EOS, T, P, Tc, Pc, omega, R_ig)
    par_EOS = resp_par_EOS['p_EOS']
    par_cubica = f_conv_param(par_EOS)
    resp_Z = f_raizes_cubica(par_cubica)
    Z_v = np.max(resp_Z['x'])
    Z_l = np.min(resp_Z['x'])
    DZ_vap_rig = Z_v - Z_l
    R_ig = 8.314 #J/mol/°C
    DH_vap_02 = - dlnPd1sT_at_T * R_ig * DZ_vap_rig
    return {'DH_vap_01': DH_vap_01, 'P_vap_T': P_vap_T, 'DZ_vap_rig': DZ_vap_rig,
            'DH_vap_02': DH_vap_02, 'dlnPd1sT_at_T': dlnPd1sT_at_T}


def f_a_EOS_mistura(a_comp, y):
  ''' Equação 14.43 p.418
  '''
  nc = y.shape[0]
  a_M = np.zeros((nc,nc))
  a = 0.0
  for i in range(0,nc):
    for j in range(0,nc):
      a_M[i,j] = np.sqrt(a_comp[i]*a_comp[j])
      a = a + y[i]*y[j]*a_M[i,j]
  return {'a': a, 'a_M': a_M}


def f_b_EOS_mistura(b_comp, y):
  ''' Equação 14.42 p.418
  '''
  b = b_comp @ y
  return b


def f_q_EOS_mistura(T, R, a, b):
  ''' Equação 14.41 p.417
  '''
  q = a / (b*R*T)
  return q


def f_beta_EOS_mistura(T, P, R, b):
  ''' Equação 14.40 p.417
  '''
  beta = (b*P) / (R*T)
  return beta


def f_calc_param_EOS_mistura(i_EOS, y, T, P, Tc_comp, Pc_comp, omega_comp, R_ig):
  nc = Tc_comp.shape[0]
  #
  Tr_comp    = np.zeros((nc,))
  Pr_comp    = np.zeros((nc,))
  alpha_comp = np.zeros((nc,))
  beta_comp  = np.zeros((nc,))
  a_comp     = np.zeros((nc,))
  b_comp     = np.zeros((nc,))
  #
  for i in range(0,nc):
    Tr_comp[i]     = T/Tc_comp[i]
    Pr_comp[i]     = P/Pc_comp[i]
    resp_param_EOS = f_param_EOS_generalizada(i_EOS,T,P,Tc_comp[i],Pc_comp[i],omega_comp[i],R_ig)
    alpha_comp[i]  = resp_param_EOS['alpha']
    beta_comp[i]   = resp_param_EOS['beta']
    a_comp[i]      = resp_param_EOS['a']
    b_comp[i]      = resp_param_EOS['b']
  #
  resp_param_EOS = f_param_EOS_generalizada(i_EOS, T, P,Tc_comp[0],Pc_comp[0],omega_comp[0],R_ig)
  Psi     = resp_param_EOS['Psi']
  sigma   = resp_param_EOS['sigma']
  epsilon = resp_param_EOS['epsilon']
  Omega   = resp_param_EOS['Omega']
  #
  a    = f_a_EOS_mistura(a_comp, y)['a']
  b    = f_b_EOS_mistura(b_comp, y)
  q    = f_q_EOS_mistura(T, R_ig, a, b)
  beta = f_beta_EOS_mistura(T, P, R_ig, b)
  #
  param_EOS = np.array([beta, q, epsilon, sigma])
  #
  saida = {'Tr_comp': Tr_comp, 'Pr_comp': Pr_comp, 'alpha_comp': alpha_comp,
           'beta_comp': beta_comp, 'a_comp': a_comp, 'b_comp': b_comp,
           'param_EOS': param_EOS, 'Psi': Psi, 'Omega': Omega }
  #
  return saida


def fdK(i,j):
  ''' Função para calcular o delta de Kronecker
  '''
  if (i == j):
    dK = 1.0
  else:
    dK = 0.0
  return dK


def f_a_bar_eq_14_45(a_comp, y):
  nc = len(y)
  resp = f_a_EOS_mistura(a_comp, y)
  a   = resp['a']
  a_M = resp['a_M']
  a_bar = np.ones((nc,))
  a_bar = a_bar*a
  for k in range(0,nc):
    soma = 0.0
    for i in range(0,nc):
      for j in range(0,nc):
        parc1 = fdK(i,k)*a_M[i,j]*y[j]
        parc2 = fdK(j,k)*a_M[i,j]*y[i]
        parc3 = -2.0*y[i]*y[j]*a_M[i,j]
        soma = soma + parc1 + parc2 + parc3
    a_bar[k] = a_bar[k] + soma
  return a_bar


def f_q_bar_eq_14_51(T, R_ig, a_comp, b_comp, y):
  nc = len(y)
  #
  a_bar = f_a_bar_eq_14_45(a_comp, y)
  resp  = f_a_EOS_mistura(a_comp, y)
  a     = resp['a']
  b_bar = b_comp.copy()
  b     = f_b_EOS_mistura(b_comp, y)
  q     = f_q_EOS_mistura(T, R_ig, a, b)
  #
  q_bar = np.zeros((nc,))
  for k in range(0,nc):
    parc1 = a_bar[k]/a
    parc2 = - b_bar[k]/b
    q_bar[k] = q*(1.0 + parc1 + parc2)
  return {'q_bar': q_bar, 'a_bar': a_bar, 'b_bar': b_bar}


def f_phi_chapeu_EOS_eq_14_50(Z, T, P, R_ig, a_comp, b_comp, y, param_EOS):
  nc = len(y)
  resp = f_q_bar_eq_14_51(T, R_ig, a_comp, b_comp, y)
  #a_bar = resp['a_bar']
  #b_bar = resp['b_bar']
  q_bar = resp['q_bar']
  b     = f_b_EOS_mistura(b_comp, y)
  beta  = f_beta_EOS_mistura(T, P, R_ig, b)
  I     = f_int_I(Z, param_EOS)
  #
  phi_chapeu = np.zeros((nc,))
  for k in range(0,nc):
    parc1 = (b_comp[k]/b)*(Z - 1.0)
    parc2 = -np.log(Z - beta)
    parc3 = -q_bar[k]*I
    phi_chapeu[k] = np.exp(parc1 + parc2 + parc3)
  return phi_chapeu


def f_Pvap_Antoine_db(Temp, i_comp, dados):
    #import numpy as np
    ''' Função que calcula a pressão de vapor, segundo a equação de Antoine, para o componente
      i_comp presente no databank_properties.pickle.
      Equação de Antoine: Pvap = exp(A - B /(Temp + C)), com: 
      [Temp] = K
      [Pvap] = mmHg
      Entrada (argumentos da função)
      Temp   = temperatura em K para a qual será calculada a Pvap
      i_comp = inteiro que corresponde ao número do componente no banco de dados
               campo/column/key = 'num'
      dados  = pandas dataframe com os dados lidos do arquivo
      Saida: tupla
      Pvap - pressão de vapor do i_comp em mmHg
      par = dicionário com os parâmetros A, B e C da equação de Antoine
    '''
    # param <- as.numeric(param)
    par_array = np.array(dados[dados['num'] == i_comp][['pvap_a','pvap_b','pvap_c']])[0]
    par = {'a': par_array[0], 'b': par_array[1], 'c': par_array[2]}
    a = par['a']
    b = par['b']
    c = par['c']
    Pvap = np.exp(a - b/(Temp + c))
    # attr(x = Pvap, which = "units") <- "mmHg"
    return Pvap, par


def f_Pvap_Antoine_vetor_db(Temp, lista_componentes, dados):
    ''' Calcula a pressão de vapor utilizando o modelo de Antoine para
          todos os componentes da lista_componentes utilizando as constantes
          do banco de dados
        Entrada:
        Temp - temperatura em K
        lista_componentes - lista com os números de identificação dos componentes
                          do sistema correspondente ao 
                          databank_properties.pickle (nc)
        dados             - dataframe com os dados do databank
        Saida:
        Pvap_comp - vetor com as P_vap dos componentes em mmHg (nc)
    '''
    nc = len(lista_componentes)
    Pvap_comp = np.zeros((nc,))
    i = 0
    for i_comp in lista_componentes:
      Pvap_comp[i] = f_Pvap_Antoine_db(Temp, i_comp, dados)[0]
      i += 1
    return Pvap_comp


def f_phi_sat_comp(T, i_EOS, lista_componentes, dados):
    nc = len(lista_componentes)
    R_ig = 83.14 # bar*cm3/mol/K
    # Obtendo: Tc, Pc_ omega
    Tc_comp = dados[dados['num'].isin(lista_componentes)]['critical_temp'].to_numpy()
    Pc_comp = dados[dados['num'].isin(lista_componentes)]['critical_pressure'].to_numpy()*(1.01325/1.0)
    om_comp = dados[dados['num'].isin(lista_componentes)]['acentric_factor'].to_numpy()
    # Calculando a P_vap dos componente puros at T
    P_sat_comp_bar = f_Pvap_Antoine_vetor_db(T, lista_componentes,dados)*(1.0133/760.0)
    #
    phi_sat = np.zeros((nc,))
    for i in range(0,nc):
        resp_param_puro = f_param_EOS_generalizada(i_EOS,T, P_sat_comp_bar[i], 
                                                Tc_comp[i], Pc_comp[i], 
                                                om_comp[i], R_ig)
        param_EOS_puro    = resp_param_puro['p_EOS']
        param_cubica_puro = f_conv_param(param_EOS_puro)
        Z_EOS_puro        = f_raizes_cubica(param_cubica_puro)['x']
        Z_vap_puro        = np.max(Z_EOS_puro)
        phi_sat_puro      = f_phi_EOS_eq_11_37(Z_vap_puro, param_EOS_puro)
        #
        phi_sat[i] = phi_sat_puro
    #
    return phi_sat



# Parei na linha 787 de funcoes_uteis_TEQ_v019.R