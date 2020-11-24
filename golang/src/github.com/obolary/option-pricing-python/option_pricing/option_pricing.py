# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# File Contains: Python code containing closed-form solutions for the valuation of European Options,
# American Options, Asian Options, Spread Options, Heat Rate Options, and Implied Volatility
#
# This document demonstrates a Python implementation of some option models described in books written by Davis
# Edwards: "Energy Trading and Investing", "Risk Management in Trading", "Energy Investing Demystified".
#
# for backward compatability with Python 2.7
from __future__ import division

# import necessary libaries
import unittest
import math
import numpy as np
from scipy.stats import norm
from scipy.stats import mvn

# Developer can toggle _DEBUG to True for more messages
# normally this is set to False
_DEBUG = False

# %% [markdown]
# MIT License
# 
# Copyright (c) 2017 Davis William Edwards
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# 
# %% [markdown]
# # Closed Form Option Pricing Formulas
# ## Generalized Black Scholes (GBS) and similar models
# %% [markdown]
# ** ChangeLog: **
# 
# * 1/1/2017 Davis Edwards, Created GBS and Asian option formulas
# * 3/2/2017 Davis Edwards, added TeX formulas to describe calculations
# * 4/9/2017 Davis Edwards, added spread option (Kirk's approximation)
# * 5/10/2017 Davis Edwards, added graphics for sensitivity analysis
# * 5/18/2017 Davis Edwards, added Bjerksund-Stensland (2002) approximation for American Options
# * 5/19/2017 Davis Edwards, added implied volatility calculations
# * 6/7/2017 Davis Edwards, expanded sensitivity tests for American option approximation.
# * 6/21/2017 Davis Edwards, added documentation for Bjerksund-Stensland models
# * 7/21/2017 Davis Edwards, refactored all of the functions to match the parameter order to Haug's "The Complete Guide to Option Pricing Formulas".
# 
# ** TO DO List **
# 1. Since the Asian Option valuation uses an approximation, need to determine the range of acceptable stresses that can be applied to the volatility input
# 2. Sub-class the custom assertions in this module to work with "unittest"
# 3. Update the greek calculations for American Options - currently the Greeks are approximated by the greeks from GBS model.
# 4. Add a bibliography referencing the academic papers used as sources
# 5. Finish writing documentation formulas for Close-Form approximation for American Options
# 6. Refactor the order of parameters for the function calls to replicate the order of parameters in academic literature
# %% [markdown]
# -------------------------
# ## Purpose:
# 
# (Why these models exist)
# 
# The software in this model is intended to price particular types of financial products called "options". These are a common type of financial product and fall into the category of "financial derivative". This documentation assumes that the reader is already familiar with options terminology. The models are largely variations of the Black Scholes Merton option framework (collectively called "Black Scholes Genre" or "Generalized Black Scholes") that are used to price European options (options that can only be exercised at one point in time). This library also includes approximations to value American options (options that can be exercised prior to the expiration date) and implied volatility calculators. 
# 
# Pricing Formulas
#     1. BlackScholes()    Stock Options (no dividend yield)
#     2. Merton()          Assets with continuous dividend yield (Index Options)
#     3. Black76()         Commodity Options
#     4. GK()              FX Options (Garman-Kohlhagen)
#     5. Asian76()         Asian Options on Commodities
#     6. Kirks76()         Spread Options (Kirk's Approximation)
#     7. American()        American options
#     8. American76()      American Commodity Options
# 
# Implied Volatility Formulas
#     9.  EuroImpliedVol   Implied volatility calculator for European options
#     10. EuroImpliedVol76 Implied volatiltity calculator for European commodity options
#     11. AmerImpliedVol   Implied volatiltity calculator for American options
#     11. AmerImpliedVol76 Implied volatility calculator for American commodity options
# 
# Note:
# In honor of the Black76 model, the 76() on the end of functions indicates a commodity option.
# 
# %% [markdown]
# -------------------------
# ## Scope
# 
# (Where this model is to be used):
# 
# This model is built to price financial option contracts on a wide variety of financial commodities. These options are widely used and represent the benchmark to which other (more complicated) models are compared. While those more complicated models may outperform these models in specific areas, outperformance is relatively uncommon. By an large, these models have taken on all challengers and remain the de-facto industry standard. 
# %% [markdown]
# ## Theory:
# 
# ### Generalized Black Scholes
# Black Scholes genre option models widely used to value European options. The original “Black Scholes” model was published in 1973 for non-dividend paying stocks. This created a revolution in quantitative finance and opened up option trading to the general population. Since that time, a wide variety of extensions to the original Black Scholes model have been created. Collectively, these are referred to as "Black Scholes genre” option models. Modifications of the formula are used to price other financial instruments like dividend paying stocks, commodity futures, and FX forwards. Mathematically, these formulas are nearly identical. The primary difference between these models is whether the asset has a carrying cost (if the asset has a cost or benefit associated with holding it) and how the asset gets present valued. To illustrate this relationship, a “generalized” form of the Black Scholes equation is shown below.
# 
# The Black Scholes model is based on number of assumptions about how financial markets operate. Black Scholes style models assume:
# 
# 1.	**Arbitrage Free Markets**. Black Scholes formulas assume that traders try to maximize their personal profits and don’t allow arbitrage opportunities (riskless opportunities to make a profit) to persist. 
# 2.	**Frictionless, Continuous Markets**. This assumption of frictionless markets assumes that it is possible to buy and sell any amount of the underlying at any time without transaction costs.
# 3.	**Risk Free Rates**. It is possible to borrow and lend money at a risk-free interest rate
# 4.	**Log-normally Distributed Price Movements**. Prices are log-normally distributed and described by Geometric Brownian Motion
# 5.	**Constant Volatility**. The Black Scholes genre options formulas assume that volatility is constant across the life of the option contract. 
# 
# In practice, these assumptions are not particularly limiting. The primary limitation imposed by these models is that it is possible to (reasonably) describe the dispersion of prices at some point in the future in a mathematical equation. 
# 
# In the traditional Black Scholes model intended to price stock options, the underlying assumption is that the stock is traded at its present value and that prices will follow a random walk diffusion style process over time. Prices are assumed to start at the spot price and, on the average, to drift upwards over time at the risk free rate. The “Merton” formula modifies the basic Black Scholes equation by introducing an additional term to incorporate dividends or holding costs. The Black 76 formula modifies the assumption so that the underlying starts at some forward price rather than a spot price. A fourth variation, the Garman Kohlhagen model, is used to value foreign exchange (FX) options. In the GK model, each currency in the currency pair is discounted based on its own interest rate.
#  
# 1.	**Black Scholes (Stocks)**. In the traditional Black Scholes model, the option is based on common stock - an instrument that is traded at its present value. The stock price does not get present valued – it starts at its present value (a ‘spot price’) and drifts upwards over time at the risk free rate. 
# 2.	**Merton (Stocks with continuous dividend yield)**. The Merton model is a variation of the Black Scholes model for assets that pay dividends to shareholders. Dividends reduce the value of the option because the option owner does not own the right to dividends until the option is exercised. 
# 3.	**Black 76 (Commodity Futures)**. The Black 76 model is for an option where the underlying commodity is traded based on a future price rather than a spot price. Instead of dealing with a spot price that drifts upwards at the risk free rate, this model deals with a forward price that needs to be present valued. 
# 4.	**Garman-Kohlhagen (FX Futures)**. The Garman Kohlhagen model is used to value foreign exchange (FX) options. In the GK model, each currency in the currency pair is discounted based on its own interest rate.
# 
# An important concept of Black Scholes models is that the actual way that the underlying asset drifts over time isn't important to the valuation. Since European options can only be exercised when the contract expires, it is only the distribution of possible prices on that date that matters - the path that the underlying took to that point doesn't affect the value of the option. This is why the primary limitation of the model is being able to describe the dispersion of prices at some point in the future, not that the dispersion process is simplistic.
# 
# The generalized Black-Scholes formula can found below (see *Figure 1 – Generalized Black Scholes Formula*). While these formulas may look complicated at first glance, most of the terms can be found as part of an options contract or are prices readily available in the market.  The only term that is difficult to calculate is the implied volatility (σ). Implied volatility is typically calculated using prices of other options that have recently been traded.
# 
# >*Call Price*
# >\begin{equation}
# C = Fe^{(b-r)T} N(D_1) - Xe^{-rT} N(D_2)
# \end{equation}
# 
# >*Put Price*
# >\begin{equation}
# P = Xe^{-rT} N(-D_2) - Fe^{(b-r)T} N(-D_1)
# \end{equation}
# 
# >*with the following intermediate calculations*
# 
# >\begin{equation}
# D_1 = \frac{ln\frac{F}{X} + (b+\frac{V^2}{2})T}{V*\sqrt{T}}
# \end{equation}
# 
# >\begin{equation}
# D_2 = D_1 - V\sqrt{T}
# \end{equation}
# 
# >*and the following inputs*
# 
# >|    Symbol    |    Meaning    |
# >|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
# >|    F or S   |    **Underlying Price**. The price of the underlying asset on the valuation date. S is used commonly used to represent a spot price, F a forward price     |
# >|    X    |    **Strike Price**.   The strike, or exercise, price of the option.    |
# >|    T    |    **Time to expiration**. The time to expiration in years. This can be calculated   by comparing the time between the expiration date and the valuation date.   T   = (t_1 - t_0)/365    |
# >|    t_0    |    **Valuation Date**.   The date on which the option is being valued. For example, it might be   today’s date if the option we being valued today.    |
# >|    t_1    |    **Expiration Date**.   The date on which the option must be exercised.    |
# >|    V    |    **Volatility**.   The volatility of the underlying security. This factor usually cannot be directly observed in the market. It is most often calculated by looking at the prices for recent option transactions and back-solving a Black Scholes style equation to find the volatility that would result in the observed price. This is commonly abbreviated with the greek letter sigma,σ, although V is used here for consistency with the code below.    |
# >|    q    |    **Continuous Yield**.   Used in the Merton model, this is the continuous yield of the underlying   security. Option holders are typically not paid dividends or other payments   until they exercise the option. As a result, this factor decreases the value   of an option.    |
# >|    r    |    **Risk Free Rate**. This is expected return on a risk-free investment. This   is commonly a approximated by the yield on a low-risk government bond or the   rate that large banks borrow between themselves (LIBOR). The rate depends on   tenor of the cash flow. For example, a 10-year risk-free bond is likely to   have a different rate than a 20-year risk-free bond.[DE1]     |
# >|    rf    |    **Foreign   Risk Free Rate**. Used in the Garman Kohlhagen model, this is the risk   free rate of the foreign currency. Each currency will have a risk free rate.    |
# >*Figure 1 - Generalized Black Scholes Formula*
# 
# The correction term, b, varies by formula – it differentiates the various Black Scholes formula from one another (see *Figure 2 - GBS Cost of Carry Adjustments*). The cost of carry refers to the cost of “carrying” or holding a position. For example, holding a bond may result in earnings from interest, holding a stock may result in stock dividends, or the like. Those payments are made to the owner of the underlying asset and not the owner of the option. As a result, they reduce the value of the option.
# 
# >|    | Model            | Cost of Carry (b) |
# >|----|------------------|-------------------|
# >| 1. | BlackScholes     | b = r             |
# >| 2. | Merton           | b = r - q         |
# >| 3. | Black 1976       | b = 0             |
# >| 4. | Garman Kohlhagen | b = r - rf        |
# >| 5. | Asian            | b = 0, modified V |
# >*Figure 2 - GBS Cost of Carry Adjustment*
# 
# %% [markdown]
# ### Asian Volatility Adjustment
# 
# An Asian option is an option whose payoff is calculated using the average price of the underlying over some period of time rather than the price on the expiration date. As a result, Asian options are also called average price options. The reason that traders use Asian options is that averaging a settlement price over a period of time reduces the affect of manipulation or unusual price movements on the expiration date on the value of the option. As a result, Asian options are often found on strategically important commodities, like crude oil or in markets with intermittent trading.
# 
# The average of a set of random numbers (prices in this case) will have a lower dispersion (a lower volatility) than the dispersion of prices observed on any single day. As a result, the implied volatility used to price Asian options will usually be slightly lower than the implied volatility on a comparable European option. From a mathematical perspective, valuing an Asian option is slightly complicated since the average of a set of lognormal distributions is not itself lognormally distributed. However, a reasonably good approximation of the correct answer is not too difficult to obtain.
# 
# In the case of Asian options on futures, it is possible to use a modified Black-76 formula that replaces the implied volatility term with an adjusted implied volatility of the average price.  As long as the first day of the averaging period is in the future, the following formula can be used to value Asian options (see *Figure 3 – Asian Option Formula*).
# 
# >*Asian Adjusted Volatility*
# \begin{equation}
# V_a = \sqrt{\frac{ln(M)}{T}}
# \end{equation}
# 
# >*with the intermediate calculation*
# \begin{equation}
# M = \frac{2e^{V^2T} - 2e^{V^2T}[1+V^2(T-t)]}{V^4(T-t)^2}
# \end{equation}
# 
# >| Symbol | Meaning |
# |--------|-----------------------------------------------------------------------------------------------------------------|
# | Va | **Asian Adjusted Volatility**, This will replace the volatility (V) term in the GBS equations shown previously. |
# | T | **Time to expiration**. The time to expiration of the option (measured in years).  |
# | t | **Time to start of averaging period**. The time to the start of the averaging period (measured in years). |
# 
# >*Figure 3 - Asian Option Formula*
# 
# %% [markdown]
# ### Spread Option (Kirk's Approximation) Calculation
# 
# Spread options are based on the spread between two commodity prices. They are commonly used to model physical investments as "real options" or to mark-to-market contracts that hedge physical assets. For example, a natural gas fueled electrical generation unit can be used to convert fuel (natural gas) into electricity. Whenever this conversion is profitable, it would be rational to operate the unit. This type of conversion is readily modeled by a spread option. When the spread of (electricity prices - fuel costs) is greater than the conversion cost, then the unit would operate. In this example, the conversion cost, which might be called the *Variable Operations and Maintenance* or VOM for a generation unit, would represent the strike price.
# 
# Analytic formulas similar to the Black Scholes equation are commonly used to value commodity spread options. One such formula is called *Kirk’s approximation*. While an exact closed form solution does not exist to value spread options, approximate solutions can give reasonably accurate results.  Kirk’s approximation uses a Black Scholes style framework to analyze the joint distribution that results from the ratio of two log-normal distributions.
# 
# In a Black Scholes equation, the distribution of price returns is assumed to be normally distributed on the expiration date. Kirk’s approximation builds on the Black Scholes framework by taking advantage of the fact that the ratio of two log-normal distributions is approximately normally distributed.  By modeling a ratio of two prices rather than the spread between the prices, Kirk’s approximation can use the same formulas designed for options based on a single underlying. In other words, Kirk’s approximation uses an algebraic transformation to fit the spread option into the Black Scholes framework.
# 
# The payoff of a spread option is show in *Figure 4 - Spread Option Payoff*.
# 
# 
# >\begin{equation}
# C = max[F_1 - F_2 - X, 0]
# \end{equation}
# 
# >\begin{equation}
# P = max[X - (F_1 - F_2), 0]
# \end{equation}
# 
# >where
# 
# >| Symbol | Meaning |
# |--------|----------------------------------------------------|
# | F_1 | **Price of Asset 1**, The prices of the first asset.  |
# | F_2 | **Price of Asset 2**. The price of the second asset.  |
# 
# 
# >*Figure 4 - Spread Option Payoff*
# 
# This can be algebraically manipulated as shown in *Figure 5 - Spread Option Payoff, Manipulated*.
# 
# >\begin{equation}
# C = max \biggl[\frac{F_1}{F_2+X}-1,0 \biggr](F_2 + X)
# \end{equation}
# 
# >\begin{equation}
# P = max \biggl[1-\frac{F_1}{F_2+X},0 \biggr](F_2 + X)
# \end{equation}
# >*Figure 5 - Spread Option Payoff, Manipulated*
# 
# This allows Kirk’s approximation to model the distribution of the spread as the ratio of the price of asset 1 over the price of asset 2 plus the strike price. This ratio can then be converted into a formula very similar to the Generalized Black Scholes formulas. In fact, this is the Black Scholes formula shown above with the addition of a (F_2 + X) term (See *Figure 6 – Kirk’s Approximation Ratio*).
# 
# >*Ratio of prices*
# >\begin{equation}
# F = \frac{F_1}{F_2 + X}
# \end{equation}
# 
# >The ratio implies that the option is profitable to exercise (*in the money*) whenever the ratio of prices (F in the formula above) is greater than 1. This occurs the cost of the finished product (F_1) exceeds total cost of the raw materials (F_2) and the conversion cost (X). This requires a modification to the Call/Put Price formulas and to the D_1 formula. Because the option is in the money when F>1, the "strike" price used in inner square brackets of the Call/Put Price formulas and the D1 formula is set to 1.
# 
# >*Spread Option Call Price*
# >\begin{equation}
# C = (F_2 + X)\biggl[Fe^{(b-r)T} N(D_1) - e^{-rT} N(D_2)\biggr]
# \end{equation}
# 
# >*Spread Option Put Price*
# >\begin{equation}
# P = (F_2 + X)\biggl[e^{-rT} N(-D_2) - Fe^{(b-r)T} N(-D_1)\biggr]
# \end{equation}
# 
# >\begin{equation}
# D_1 = \frac{ln(F) + (b+\frac{V^2}{2})T}{V*\sqrt{T}}
# \end{equation}
# 
# >\begin{equation}
# D_2 = D_1 - V\sqrt{T}
# \end{equation}
# 
# >*Figure 6- Kirk's Approximation Ratio*
# 
# The key complexity is determining the appropriate volatility that needs to be used in the equation. The “approximation” which defines Kirk’s approximation is the assumption that the ratio of two log-normal distributions is normally distributed. That assumption makes it possible to estimate the volatility needed for the modified Black Scholes style equation. (See *Figure 7 - Kirk's Approximation (Volatility)*).
# 
# >\begin{equation}
# V = \sqrt{ V_1^{2}+ \biggl[V_2\frac{F_2}{F_2+X}\biggr]^2 - 2ρ V_1 V_2 \frac{F_2}{F_2+X} }
# \end{equation}
# 
# >|    Symbol    |    Meaning    |
# >|--------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
# >|    V   |    **Volatility**. The Kirk's approximation volatility that will be placed into the formula shown in Figure 6    |
# >|    V1    |    **Volatility of Asset 1**.   The strike, or exercise, price of the option.    |
# >|    V2    |    **Volatility of Asset 2**. The volatility of the second asset   |
# >|    ρ    |    **Correlation**. The correlation between price of asset 1 and the price of asset 2.    |
# 
# >*Figure 7- Kirk's Approximation (Volatility)*
# 
# A second complexity is that the prices of two assets (F1 and F2) have to be in the same units. For example, in a heat rate option, the option represents the ability to convert fuel (natural gas) into electricity. The price of the first asset, electricity, might be quoted in US dollars per megawatt-hour or USD/MWH. However, the price of the second asset might be quoted in USD/MMBTU. To use the approximation, it is necessary to convert the price of the second asset into the units of the first asset (See *Example 1 - a Heat Rate Option*). This conversion rate will typically be specified as part of the contract.
# 
# >Example: A 10 MMBTU/MWH heat rate call option
# >* F1 = price of electricity = USD 35/MWH
# >* F2* = price of natural gas = USD 3.40/MMBTU; *This is not the price to plug into the model!*
# >* V1 = volatility of electricity forward prices = 35%
# >* V2 = volatility of natural gas forward price = 35%
# >* Rho = correlation between electricity and natural gas forward prices = 90%
# >* VOM = variable operation and maintenance cost (the conversion cost) = USD 3/MWH
# 
# >Before being placed into a spread option model, the price of natural gas would need to 
# >be converted into the correct units.
# >* F2 = Heat Rate * Fuel Cost = (10 MMBTU/MWH)(USD 3.40/MMBTU) = USD 34/MWH
# 
# >The strike price would be set equal to the conversion cost
# >* X = VOM costs = USD 3/MWH
# 
# > *Example 1 - a Heat Rate Call Option*
# 
# Another important consideration (not discussed in this write-up) is that volatility and correlation need to be matched to the tenor of the underlying assets. This means that it is necessary to measure the volatility of forward prices rather than spot prices. It may also be necessary to match the volatility and correlation to the correct month. For example, power prices in August may behave very differently than power prices in October or May in certain regions.  
# 
# Like any model, spread options are subject to the "garbage in = garbage out" problem. However, the relative complexity of modeling commodity prices (the typical underlying for spread options) makes calibrating inputs a key part of the model.
# 
# %% [markdown]
# ### American Options
# American options differ from European options because they can be exercised at any time. If there is a possibility that it will be more profitable to exercise the option than sell it, an American option will have more value than a corresponding European option. Early exercise typically occurs only when an option is *in the money*. If an option is out of the money, there is usually no reason to exercise early - it would be better to sell the option (in the case of a put option, to sell the option and the underlying asset).
# 
# The decision of whether to exercise early is primarily a question of interest rates and carrying costs. Carrying costs, or *cost of carry*, is a term that means an intermediate cash flows that is the result of holding an asset. For example, dividends on stocks are a postive cost of carry (owning the asset gives the owner a cash flow). A commodity might have a negative cost of carry. For example, a commodity that requires its owner to pay for storage would cause the owner of the physical commodity to pay cash to hold the asset. (**Note:** Commodity options are typically written on forwards or futures which have zero cost of carry instead of the actual underlying commodity). Cost of carry is cash flow that affects the owner of the underlying commodity and not the owner of the option. For example, when a stock pays a dividend, the owner of a call option does not receive the dividend - just the owner of the stock. For the perspective for the owner of a call option on a stock, the cost of carry will be the interest received from holding cash (r) less any dividends paid to owners of the stock (q).
# 
# Since an option has some value (the *extrinsic value*) that would be given up by exercising the option, exercising an option prior to maturity is a trade off between the option's extrinsic value (the remaining optionality) and the relative benefit of holding cash (time value of money) versus the benefit of holding the asset (carrying costs). 
# 
# The early exercise feature of **American equity put options** may have value when:
# * The cost of carry on the asset is low - preferably zero or negative. 
# * Interest rates are high  
# * The option is in the money
# 
# The early exercise feature of **American equity call options** may have value when:
# * The cost of carry on the asset is positive
# * Interest rates are low or negative
# * The option is in the money 
# 
# With commodities, things are a slightly different. There is typically no cost of carry since the underlying is a forward or a futures contract. It does not cost any money to enter an at-the-money commodity forward, swap, or futures contract. Also, these contracts don't have any intermediate cash flows. As a result, the primary benefit of early exercise is to get cash immediately (exercising an in-the-money option) rather than cash in the future. In high interest rate environements, the money recieved immediately from immediate execution may exceed the extrinsic value of the contract. This is due to strike price not being present valued in immediate execution (it is specified in the contract and a fixed number) but the payoff of a European option is discounted (forward price - strike price). 
# 
# The overall result is that early exercise is fairly uncommon for most commodity options. Typically, it only occurs when interest rates are high. Generally, interest rates have to be higher than 15%-20% for American commodity options to differ substantially in value from European options with the same terms.
# 
# The early exercise feature of **American commodity options** has value when:
# * Interest rates are high
# * Volatility is low (this makes selling the option less of a good option)
# * The option is in the money 
# 
# There is no exact closed-form solution for American options. However, there are many approximations that are reasonably close to prices produced by open-form solutions (like binomial tree models). Two models are shown below, both created by Bjerksund and Stensland. The first was produced in 1993 and the second in 2002. The second model is a refinement of the first model, adding more complexity, in exchange for better accuracy. 
# %% [markdown]
# #### Put-Call Parity
# Because of Put/Call parity, it is possible to use a call valuation formula to calculate the value of a put option.
# 
# >\begin{equation}
# P(S,X,T,r,b,V) = C(X,S,T,r-b,-b,V)
# \end{equation}
# 
# or using the order of parameters used in this library:
# 
# >\begin{equation}
# P(X,S,T,b,r,V) = C(S,X,T,-b,r-b,V)
# \end{equation}
# 
# %% [markdown]
# #### BjerksundStensland 1993 (BS1993)
# There is no closed form solution for American options, and there are multiple people who have developed closed-form approximations to value American options. This is one such approximation. However, this approximation is no longer in active use by the public interface. It is primarily included as a secondary test on the BS2002 calculation. This function uses a numerical approximation to estimate the value of an American option. It does this by estimating a early exercise boundary and analytically estimating the probability of hitting that boundary. This uses the same inputs as a Generalized Black Scholes model:
# 
#     FS = Forward or spot price (abbreviated FS in code, F in formulas below)
#     X = Strike Price
#     T = time to expiration
#     r = risk free rate 
#     b = cost of carry 
#     V = volatility
# 
# _Intermediate Calculations_. To be consistent with the Bjerksund Stensland paper, this write-up uses similar notation. Please note that both a capital B (B_0 and B_Infinity), a lower case b, and the greek symbol Beta are all being used. B_0 and B_infinity represent that optimal exercise boundaries in edge cases (for call options where T=0 and T=infinity respectively), lower case b is the cost of carry (passed in as an input), and Beta is an intermediate calculations.
# 
# >\begin{array}{lcl}
# \beta & = & (0.5 - \frac{b}{V^2}) + \sqrt{(\frac{b}{V^2} - 0.5)^2 + 2 \frac{r}{V^2}} \\
# B_\infty & = & \frac{\beta}{\beta-1} X \\
# B_0 & = & max\biggl[X, (\frac{r}{r-b}) X\biggr] \\
# h_1 & = & - b T + 2 V \sqrt{T} \frac{B_0}{B_\infty-B_0} \\
# \end{array}
# 
# _Calculate the Early Exercise Boundary (i)_. The lower case i represents the early exercise boundary. Alpha is an intermediate calculation.
# 
# >\begin{array}{lcl}
# i & = & B_0 + (B_\infty-B_0)(1 - e^{h_1} ) \\
# \alpha & = & (i-X) i^{-\beta}
# \end{array}
# 
# Check for immediate exercise_.
# 
# >\begin{equation}
# if F >= i, then Value = F - X
# \end{equation}
# 
# If no immediate exercise, approximate the early exercise price.
# 
# >\begin{eqnarray}
# Value & = & \alpha * F^\beta \\
# & - & \alpha * \phi(F,T,\beta,i,i,r,b,V) \\
# & + & \phi(F,T,1,i,i,r,b,V) \\
# & - & \phi(F,T,1,X,i,r,b,V) \\
# & - & X * \phi(F,T,0,i,i,r,b,V) \\
# & + & X * \phi(F,T,0,X,i,r,b,V)
# \end{eqnarray}
# 
# _Compare to European Value_. Due to the approximation, it is sometime possible to get a value slightly smaller than the European value. If so, set the value equal to the European value estimated using Generalized Black Scholes.
# 
# >\begin{equation}
# Value_{BS1993} = Max \biggl[ Value, Value_{GBS} \biggr]
# \end{equation}
# %% [markdown]
# #### Bjerksund Stensland 2002 (BS2002)
# source: https://www.researchgate.net/publication/228801918
# 
#     FS = Forward or spot price (abbreviated FS in code, F in formulas below)
#     X = Strike Price
#     T = time to expiration
#     r = risk free rate 
#     b = cost of carry 
#     V = volatility
# %% [markdown]
# #### Psi
# Psi is an intermediate calculation used by the Bjerksund Stensland 2002 approximation.
# 
# \begin{equation}
# \psi(F, t_2, \gamma, H, I_2, I_1, t_1, r, b, V)
# \end{equation}
# 
# _Intermediate calculations_.
# The Psi function has a large number of intermediate calculations. For clarity, these are loosely organized into groups with each group used to simplify the next set of intermediate calculations.
# 
# >\begin{array}{lcl}
# A_1 & = & V \ln(t_1) \\
# A_2 & = & V \ln(t_2) \\
# B_1 & = & \biggl[ b+(\gamma-0.5) V^2 \biggr] t_1 \\
# B_2 & = & \biggl[ b+(\gamma-0.5) V^2 \biggr] t_2 
# \end{array}   
# 
# More Intermediate calculations
# >\begin{array}{lcl}
# d_1 & = & \frac{ln(\frac{F}{I_1}) + B_1}{A_1} \\
# d_2 & = & \frac{ln(\frac{I_2^2}{F I_1}) + B_1}{A_1} \\
# d_3 & = & \frac{ln(\frac{F}{I_1}) - B_1}{A_1} \\
# d_4 & = & \frac{ln(\frac{I_2^2}{F I_1}) - B_1}{A_1} \\
# e_1 & = & \frac{ln(\frac{F}{H}) + B_2}{A_2} \\
# e_2 & = & \frac{ln(\frac{I_2^2}{F H}) + B_2}{A_2} \\
# e_3 & = & \frac{ln(\frac{I_1^2}{F H}) + B_2}{A_2} \\
# e_4 & = & \frac{ln(\frac{F I_1^2}{H I_2^2}) + B_2}{A_2}
# \end{array}
# 
# Even More Intermediate calculations
# >\begin{array}{lcl}
# \tau & = & \sqrt{\frac{t_1}{t_2}} \\
# \lambda & = & -r+\gamma b+\frac{\gamma}{2} (\gamma-1) V^2 \\
# \kappa & = & \frac{2b}{V^2} +(2 \gamma - 1)
# \end{array}
# 
# _The calculation of Psi_.
# This is the actual calculation of the Psi function. In the function below, M() represents the cumulative bivariate normal distribution (described a couple of paragraphs below this section). The abbreviation M() is used instead of CBND() in this section to make the equation a bit more readable and to match the naming convention used in Haug's book "The Complete Guide to Option Pricing Formulas".
# 
# >\begin{eqnarray}
# \psi & = & e^{\lambda t_2} F^\gamma M(-d_1, -e_1, \tau) \\
# & - & \frac{I_2}{F}^\kappa M(-d_2, -e_2, \tau) \\
# & - & \frac{I_1}{F}^\kappa M(-d_3, -e_3, -\tau) \\
# & + & \frac{I_1}{I_2}^\kappa M(-d_4, -e_4, -\tau))
# \end{eqnarray}
# 
# 
# %% [markdown]
# #### Phi
# Phi is an intermediate calculation used by both the Bjerksun Stensland 1993 and 2002 approximations. Many of the parameters are the same as the GBS model.
# 
# \begin{equation}
# \phi(FS, T, \gamma, h, I, r, b, V)
# \end{equation}
# 
#     FS = Forward or spot price (abbreviated FS in code, F in formulas below).
#     T = time to expiration. 
#     I =  trigger price (as calculated in either BS1993 or BS2002 formulas
#     gamma = modifier to T, calculated in BS1993 or BS2002 formula
#     r = risk free rate. 
#     b = cost of carry. 
#     V = volatility. 
# 
# Internally, the Phi() function is implemented as follows:
# 
# >\begin{equation}
# d_1 = -\frac{ln(\frac{F}{h}) + \biggl[b+(\gamma-0.5) V^2 \biggr] T}{V \sqrt{T}}
# \end{equation}
# 
# >\begin{equation}
# d_2 = d_1 - 2 \frac{ln(I/F)}{V \sqrt(T)}
# \end{equation}
# 
# >\begin{equation}
# \lambda = -r+\gamma b+0.5 \gamma (\gamma-1) V^2
# \end{equation}
# 
# >\begin{equation}
# \kappa = \frac{2b}{V^2}+(2\gamma-1)
# \end{equation}
# 
# >\begin{equation}
# \phi = e^{\lambda T} F^{\gamma} \biggl[ N(d_1)-\frac{I}{F}^{\kappa} N(d_2) \biggr]
# \end{equation}
# %% [markdown]
# ##### Normal Cumulative Density Function (N)
# This is the normal cumulative density function. It can be found described in a variety of statistical textbooks and/or wikipedia. It is part of the standard scipy.stats distribution and imported using the "from scipy.stats import norm" command.
# 
# Example:
# \begin{equation}
#     N(d_1)
# \end{equation}
# %% [markdown]
# #### Cumulative bivariate normal distribution (CBND)
# The bivariate normal density function (BNDF) is given below (See *Figure 8 - Bivariate Normal Density Function (BNDF)*):
# >\begin{equation}
# BNDF(x, y) =  \frac{1}{2 \pi \sqrt{1-p^2}} exp \biggl[-\frac{x^2-2pxy+y^2}{2(1-p^2)}\biggr]
# \end{equation}
# >*Figure 8. Bivariate Normal Density Function (BNDF)*
# 
# This can be integrated over x and y to calculate the joint probability that x < a and y < b. This is called the cumulative bivariate normal distribution (CBND) (See *Figure 9 - Cumulative Bivariate Normal Distribution (CBND))*: 
# >\begin{equation}
# CBND(a, b, p) = \frac{1}{2 \pi \sqrt{1-p^2}} \int_{-\infty}^{a} \int_{-\infty}^{b} exp \biggl[-\frac{x^2-2pxy+y^2}{2(1-p^2)}\biggr] d_x d_y
# \end{equation}
# >*Figure 9. Cumulative Bivariate Normal Distribution (CBND)*
# 
# Where
# * x = the first variable
# * y = the second variable
# * a = upper bound for first variable
# * b = upper bound for second variable
# * p = correlation between first and second variables
# 
# There is no closed-form solution for this equation. However, several approximations have been developed and are included in the numpy library distributed with Anaconda. The Genz 2004 model was chosen for implementation. Alternative models include those developed by Drezner and Wesolowsky (1990) and Drezner (1978). The Genz model improves these other model by going to an accuracy of 14 decimal points (from approximately 8 decimal points and 6 decimal points respectively). 
# %% [markdown]
# -------------------------
# ## Limitations:
# These functions have been tested for accuracy within an allowable range of inputs (see "Model Input" section below). However, general modeling advice applies to the use of the model. These models depend on a number of assumptions. In plain English, these models assume that the distribution of future prices can be described by variables like implied volatility. To get good results from the model, the model should only be used with reliable inputs.
# 
# The following limitations are also in effect:
# 
# 1. The Asian Option approximation shouldn't be used for Asian options that are into the Asian option calculation period.
# 2. The American and American76 approximations break down when r < -20%. The limits are set wider in this example for testing purposes, but production code should probably limit interest rates to values between -20% and 100%. In practice, negative interest rates should be extremely rare.
# 3. No greeks are produced for spread options
# 4. These models assume a constant volatility term structure. This has no effect on European options. However, options that are likely to be exercise early (certain American options) and Asian options may be more affected. 
# %% [markdown]
# -------------------------
# ## Model Inputs
# This section describes the function calls an inputs needed to call this model:
# 
# These functions encapsulate the most commonly encountered option pricing formulas. These function primarily figure out the cost-of-carry term (b) and then call the generic version of the function. All of these functions return an array containg the premium and the greeks.
# 
# #### Public Functions in the Library
# 
# Pricing Formulas:
#     1. BlackScholes (OptionType, X, FS, T, r, V)
#     2. Merton (OptionType, X, FS, T, r, q, V)
#     3. Black76 (OptionType, X, FS, T, r, V)
#     4. GK (OptionType, X, FS, T, b, r, rf, V)
#     5. Asian76 (OptionType, X, FS, T, TA, r, V)
#     6. Kirks76
#     7. American (OptionType, X, FS, T, r, q, V)
#     8. American76 (OptionType, X, FS, T, r, V)
# 
# Implied Volatility Formulas
#     9. GBS_ImpliedVol(OptionType, X, FS, T, r, q, CP)
#     10. GBS_ImpliedVol76(OptionType, X, FS, T, r, CP)
#     11. American_ImpliedVol(OptionType, X, FS, T, r, q, CP)
#     11. American_ImpliedVol76(OptionType, X, FS, T, r, CP)
#     
# #### Inputs used by all models
# | **Parameter** | **Description**                                                                                                                                      |
# |---------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
# | option_type   | **Put/Call Indicator** Single character, "c" indicates a call; "p" a put|
# | fs            | **Price of Underlying** FS is generically used, but for specific models, the following abbreviations may be used: F = Forward Price, S = Spot Price) |
# | x             | **Strike Price** |
# | t             | **Time to Maturity** This is in years (1.0 = 1 year, 0.5 = six months, etc)|
# | r             | **Risk Free Interest Rate** Interest rates (0.10 = 10% interest rate |
# | v             | **Implied Volatility** Annualized implied volatility (1=100% annual volatility, 0.34 = 34% annual volatility|
# 
# #### Inputs used by some models
# | **Parameter** | **Description**                                                                                                                                      |
# |---------------|------------------------------------------------------------------------------------------------------------------------------------------------------|
# | b             | **Cost of Carry** This is only found in internal implementations, but is identical to the cost of carry (b) term commonly found in academic option pricing literature|
# | q             | **Continuous Dividend** Used in Merton and American models; Internally, this is converted into cost of carry, b, with formula b = r-q                |
# | rf            | **Foreign Interest Rate** Only used GK model; this functions similarly to q                                                                          |
# | t_a             | **Asian Start** Used for Asian options; This is the time that starts the averaging period (TA=0 means that averaging starts immediately). As TA approaches T, the Asian value should become very close to the Black76 Value |
# | cp             | **Option Price** Used in the implied vol calculations; This is the price of the call or put observed in the market |
# 
# 
# #### Outputs
# All of the option pricing functions return an array. The first element of the array is the value of the option, the other elements are the greeks which measure the sensitivity of the option to changes in inputs. The greeks are used primarily for risk-management purposes.
# 
# | **Output** | **Description**                                                                                                   |
# |------------|-------------------------------------------------------------------------------------------------------------------|
# | [0]        | **Value**                                                                                                         |
# | [1]        | **Delta**  Sensitivity of Value to changes in price                                                               |
# | [2]        | **Gamma** Sensitivity of Delta to changes in price                                                                |
# | [3]        | **Theta** Sensitivity of Value to changes in time to expiration (annualized). To get a daily Theta, divide by 365 |
# | [4]        | **Vega** Sensitivity of Value to changes in Volatility                                                            |
# | [5]        | **Rho** Sensitivity of Value to changes in risk-free rates.                                                       |
# 
# The implied volatility functions return a single value (the implied volatility).
# 
# #### Acceptable Range for inputs
# All of the inputs are bounded. While many of these functions will work with inputs outside of these bounds, they haven't been tested and are generally believed to be uncommon. The pricer will return an exception to the caller if an out-of-bounds input is used. If that was a valid input, the code below will need to be modified to allow wider inputs and the testing section updated to test that the models work under the widened inputs.

# %%
# This class contains the limits on inputs for GBS models
# It is not intended to be part of this module's public interface
class _GBS_Limits:
    # An GBS model will return an error if an out-of-bound input is input
    MAX32 = 2147483248.0

    MIN_T = 1.0 / 1000.0  # requires some time left before expiration
    MIN_X = 0.01
    MIN_FS = 0.01

    # Volatility smaller than 0.5% causes American Options calculations
    # to fail (Number to large errors).
    # GBS() should be OK with any positive number. Since vols less
    # than 0.5% are expected to be extremely rare, and most likely bad inputs,
    # _gbs() is assigned this limit too
    MIN_V = 0.005

    MAX_T = 100
    MAX_X = MAX32
    MAX_FS = MAX32

    # Asian Option limits
    # maximum TA is time to expiration for the option
    MIN_TA = 0

    # This model will work with higher values for b, r, and V. However, such values are extremely uncommon. 
    # To catch some common errors, interest rates and volatility is capped to 100%
    # This reason for 1 (100%) is mostly to cause the library to throw an exceptions 
    # if a value like 15% is entered as 15 rather than 0.15)
    MIN_b = -1
    MIN_r = -1

    MAX_b = 1
    MAX_r = 1
    MAX_V = 1
      
    

# %% [markdown]
# ------------------------
# ## Model Implementation
# These functions encapsulate a generic version of the pricing formulas. They are primarily intended to be called by the other functions within this libary. The following functions will have a fixed interface so that they can be called directly for academic applicaitons that use the cost-of-carry (b) notation:
# 
#     _GBS()                  A generalized European option model   
#     _American()             A generalized American option model    
#     _GBS_ImpliedVol()       A generalized European option implied vol calculator
#     _American_ImpliedVol()  A generalized American option implied vol calculator
#     
# The other functions in this libary are called by the four main functions and are not expected to be interface safe (the implementation and interface may change over time).
# %% [markdown]
# ### Implementation: European Options
# These functions implement the generalized Black Scholes (GBS) formula for European options. The main function is _gbs().

# %%
# ------------------------------
# This function verifies that the Call/Put indicator is correctly entered
def _test_option_type(option_type):
    if (option_type != "c") and (option_type != "p"):
        raise GBS_InputError("Invalid Input option_type ({0}). Acceptable value are: c, p".format(option_type))


# %%
# ------------------------------
# This function makes sure inputs are OK
# It throws an exception if there is a failure
def _gbs_test_inputs(option_type, fs, x, t, r, b, v):
    # -----------
    # Test inputs are reasonable
    _test_option_type(option_type)

    if (x < _GBS_Limits.MIN_X) or (x > _GBS_Limits.MAX_X):
        raise GBS_InputError(
            "Invalid Input Strike Price (X). Acceptable range for inputs is {1} to {2}".format(x, _GBS_Limits.MIN_X,
                                                                                               _GBS_Limits.MAX_X))

    if (fs < _GBS_Limits.MIN_FS) or (fs > _GBS_Limits.MAX_FS):
        raise GBS_InputError(
            "Invalid Input Forward/Spot Price (FS). Acceptable range for inputs is {1} to {2}".format(fs,
                                                                                                      _GBS_Limits.MIN_FS,
                                                                                                      _GBS_Limits.MAX_FS))

    if (t < _GBS_Limits.MIN_T) or (t > _GBS_Limits.MAX_T):
        raise GBS_InputError(
            "Invalid Input Time (T = {0}). Acceptable range for inputs is {1} to {2}".format(t, _GBS_Limits.MIN_T,
                                                                                             _GBS_Limits.MAX_T))

    if (b < _GBS_Limits.MIN_b) or (b > _GBS_Limits.MAX_b):
        raise GBS_InputError(
            "Invalid Input Cost of Carry (b = {0}). Acceptable range for inputs is {1} to {2}".format(b,
                                                                                                      _GBS_Limits.MIN_b,
                                                                                                      _GBS_Limits.MAX_b))

    if (r < _GBS_Limits.MIN_r) or (r > _GBS_Limits.MAX_r):
        raise GBS_InputError(
            "Invalid Input Risk Free Rate (r = {0}). Acceptable range for inputs is {1} to {2}".format(r,
                                                                                                       _GBS_Limits.MIN_r,
                                                                                                       _GBS_Limits.MAX_r))

    if (v < _GBS_Limits.MIN_V) or (v > _GBS_Limits.MAX_V):
        raise GBS_InputError(
            "Invalid Input Implied Volatility (V = {0}). Acceptable range for inputs is {1} to {2}".format(v,
                                                                                                           _GBS_Limits.MIN_V,
                                                                                                           _GBS_Limits.MAX_V))


# %%

# The primary class for calculating Generalized Black Scholes option prices and deltas
# It is not intended to be part of this module's public interface

# Inputs: option_type = "p" or "c", fs = price of underlying, x = strike, t = time to expiration, r = risk free rate
#         b = cost of carry, v = implied volatility
# Outputs: value, delta, gamma, theta, vega, rho
def _gbs(option_type, fs, x, t, r, b, v):
    _debug("Debugging Information: _gbs()")
    # -----------
    # Test Inputs (throwing an exception on failure)
    _gbs_test_inputs(option_type, fs, x, t, r, b, v)

    # -----------
    # Create preliminary calculations
    t__sqrt = math.sqrt(t)
    d1 = (math.log(fs / x) + (b + (v * v) / 2) * t) / (v * t__sqrt)
    d2 = d1 - v * t__sqrt

    if option_type == "c":
        # it's a call
        _debug("     Call Option")
        value = fs * math.exp((b - r) * t) * norm.cdf(d1) - x * math.exp(-r * t) * norm.cdf(d2)
        delta = math.exp((b - r) * t) * norm.cdf(d1)
        gamma = math.exp((b - r) * t) * norm.pdf(d1) / (fs * v * t__sqrt)
        theta = -(fs * v * math.exp((b - r) * t) * norm.pdf(d1)) / (2 * t__sqrt) - (b - r) * fs * math.exp(
            (b - r) * t) * norm.cdf(d1) - r * x * math.exp(-r * t) * norm.cdf(d2)
        vega = math.exp((b - r) * t) * fs * t__sqrt * norm.pdf(d1)
        rho = x * t * math.exp(-r * t) * norm.cdf(d2)
    else:
        # it's a put
        _debug("     Put Option")
        value = x * math.exp(-r * t) * norm.cdf(-d2) - (fs * math.exp((b - r) * t) * norm.cdf(-d1))
        delta = -math.exp((b - r) * t) * norm.cdf(-d1)
        gamma = math.exp((b - r) * t) * norm.pdf(d1) / (fs * v * t__sqrt)
        theta = -(fs * v * math.exp((b - r) * t) * norm.pdf(d1)) / (2 * t__sqrt) + (b - r) * fs * math.exp(
            (b - r) * t) * norm.cdf(-d1) + r * x * math.exp(-r * t) * norm.cdf(-d2)
        vega = math.exp((b - r) * t) * fs * t__sqrt * norm.pdf(d1)
        rho = -x * t * math.exp(-r * t) * norm.cdf(-d2)

    _debug("     d1= {0}\n     d2 = {1}".format(d1, d2))
    _debug("     delta = {0}\n     gamma = {1}\n     theta = {2}\n     vega = {3}\n     rho={4}".format(delta, gamma,
                                                                                                        theta, vega,
                                                                                                        rho))
    
    return value, delta, gamma, theta, vega, rho    

# %% [markdown]
# ### Implementation: American Options
# This section contains the code necessary to price American options. The main function is _American(). The other functions are called from the main function.

# %%
# -----------
# Generalized American Option Pricer
# This is a wrapper to check inputs and route to the current "best" American option model
def _american_option(option_type, fs, x, t, r, b, v):
    # -----------
    # Test Inputs (throwing an exception on failure)
    _debug("Debugging Information: _american_option()")
    _gbs_test_inputs(option_type, fs, x, t, r, b, v)

    # -----------
    if option_type == "c":
        # Call Option
        _debug("     Call Option")
        return _bjerksund_stensland_2002(fs, x, t, r, b, v)
    else:
        # Put Option
        _debug("     Put Option")

        # Using the put-call transformation: P(X, FS, T, r, b, V) = C(FS, X, T, -b, r-b, V)
        # WARNING - When reconciling this code back to the B&S paper, the order of variables is different

        put__x = fs
        put_fs = x
        put_b = -b
        put_r = r - b

        # pass updated values into the Call Valuation formula
        return _bjerksund_stensland_2002(put_fs, put__x, t, put_r, put_b, v)


# %%
# -----------
# American Call Option (Bjerksund Stensland 1993 approximation)
# This is primarily here for testing purposes; 2002 model has superseded this one
def _bjerksund_stensland_1993(fs, x, t, r, b, v):
    # -----------
    # initialize output
    # using GBS greeks (TO DO: update greek calculations)
    my_output = _gbs("c", fs, x, t, r, b, v)

    e_value = my_output[0]
    delta = my_output[1]
    gamma = my_output[2]
    theta = my_output[3]
    vega = my_output[4]
    rho = my_output[5]

    # debugging for calculations
    _debug("-----")
    _debug("Debug Information: _Bjerksund_Stensland_1993())")

    # if b >= r, it is never optimal to exercise before maturity
    # so we can return the GBS value
    if b >= r:
        _debug("     b >= r, early exercise never optimal, returning GBS value")
        return e_value, delta, gamma, theta, vega, rho

    # Intermediate Calculations
    v2 = v ** 2
    sqrt_t = math.sqrt(t)

    beta = (0.5 - b / v2) + math.sqrt(((b / v2 - 0.5) ** 2) + 2 * r / v2)
    b_infinity = (beta / (beta - 1)) * x
    b_zero = max(x, (r / (r - b)) * x)

    h1 = -(b * t + 2 * v * sqrt_t) * (b_zero / (b_infinity - b_zero))
    i = b_zero + (b_infinity - b_zero) * (1 - math.exp(h1))
    alpha = (i - x) * (i ** (-beta))

    # debugging for calculations
    _debug("     b = {0}".format(b))
    _debug("     v2 = {0}".format(v2))
    _debug("     beta = {0}".format(beta))
    _debug("     b_infinity = {0}".format(b_infinity))
    _debug("     b_zero = {0}".format(b_zero))
    _debug("     h1 = {0}".format(h1))
    _debug("     i  = {0}".format(i))
    _debug("     alpha = {0}".format(alpha))

    # Check for immediate exercise
    if fs >= i:
        _debug("     Immediate Exercise")
        value = fs - x
    else:
        _debug("     American Exercise")
        value = (alpha * (fs ** beta)
                 - alpha * _phi(fs, t, beta, i, i, r, b, v)
                 + _phi(fs, t, 1, i, i, r, b, v)
                 - _phi(fs, t, 1, x, i, r, b, v)
                 - x * _phi(fs, t, 0, i, i, r, b, v)
                 + x * _phi(fs, t, 0, x, i, r, b, v))

    # The approximation can break down in boundary conditions
    # make sure the value is at least equal to the European value
    value = max(value, e_value)
    return value, delta, gamma, theta, vega, rho


# %%
# -----------
# American Call Option (Bjerksund Stensland 2002 approximation)
def _bjerksund_stensland_2002(fs, x, t, r, b, v):
    # -----------
    # initialize output
    # using GBS greeks (TO DO: update greek calculations)
    my_output = _gbs("c", fs, x, t, r, b, v)

    e_value = my_output[0]
    delta = my_output[1]
    gamma = my_output[2]
    theta = my_output[3]
    vega = my_output[4]
    rho = my_output[5]

    # debugging for calculations
    _debug("-----")
    _debug("Debug Information: _Bjerksund_Stensland_2002())")

    # If b >= r, it is never optimal to exercise before maturity
    # so we can return the GBS value
    if b >= r:
        _debug("     Returning GBS value")
        return e_value, delta, gamma, theta, vega, rho

    # -----------
    # Create preliminary calculations
    v2 = v ** 2
    t1 = 0.5 * (math.sqrt(5) - 1) * t
    t2 = t

    beta_inside = ((b / v2 - 0.5) ** 2) + 2 * r / v2
    # forcing the inside of the sqrt to be a positive number
    beta_inside = abs(beta_inside)
    beta = (0.5 - b / v2) + math.sqrt(beta_inside)
    b_infinity = (beta / (beta - 1)) * x
    b_zero = max(x, (r / (r - b)) * x)

    h1 = -(b * t1 + 2 * v * math.sqrt(t1)) * ((x ** 2) / ((b_infinity - b_zero) * b_zero))
    h2 = -(b * t2 + 2 * v * math.sqrt(t2)) * ((x ** 2) / ((b_infinity - b_zero) * b_zero))

    i1 = b_zero + (b_infinity - b_zero) * (1 - math.exp(h1))
    i2 = b_zero + (b_infinity - b_zero) * (1 - math.exp(h2))

    alpha1 = (i1 - x) * (i1 ** (-beta))
    alpha2 = (i2 - x) * (i2 ** (-beta))

    # debugging for calculations
    _debug("     t1 = {0}".format(t1))
    _debug("     beta = {0}".format(beta))
    _debug("     b_infinity = {0}".format(b_infinity))
    _debug("     b_zero = {0}".format(b_zero))
    _debug("     h1 = {0}".format(h1))
    _debug("     h2 = {0}".format(h2))
    _debug("     i1 = {0}".format(i1))
    _debug("     i2 = {0}".format(i2))
    _debug("     alpha1 = {0}".format(alpha1))
    _debug("     alpha2 = {0}".format(alpha2))

    # check for immediate exercise
    if fs >= i2:
        value = fs - x
    else:
        # Perform the main calculation    
        value = (alpha2 * (fs ** beta)
                 - alpha2 * _phi(fs, t1, beta, i2, i2, r, b, v)
                 + _phi(fs, t1, 1, i2, i2, r, b, v)
                 - _phi(fs, t1, 1, i1, i2, r, b, v)
                 - x * _phi(fs, t1, 0, i2, i2, r, b, v)
                 + x * _phi(fs, t1, 0, i1, i2, r, b, v)
                 + alpha1 * _phi(fs, t1, beta, i1, i2, r, b, v)
                 - alpha1 * _psi(fs, t2, beta, i1, i2, i1, t1, r, b, v)
                 + _psi(fs, t2, 1, i1, i2, i1, t1, r, b, v)
                 - _psi(fs, t2, 1, x, i2, i1, t1, r, b, v)
                 - x * _psi(fs, t2, 0, i1, i2, i1, t1, r, b, v)
                 + x * _psi(fs, t2, 0, x, i2, i1, t1, r, b, v))

    # in boundary conditions, this approximation can break down
    # Make sure option value is greater than or equal to European value
    value = max(value, e_value)

    # -----------
    # Return Data
    return value, delta, gamma, theta, vega, rho


# %%
# ---------------------------
# American Option Intermediate Calculations

# -----------
# The Psi() function used by _Bjerksund_Stensland_2002 model
def _psi(fs, t2, gamma, h, i2, i1, t1, r, b, v):
    vsqrt_t1 = v * math.sqrt(t1)
    vsqrt_t2 = v * math.sqrt(t2)

    bgamma_t1 = (b + (gamma - 0.5) * (v ** 2)) * t1
    bgamma_t2 = (b + (gamma - 0.5) * (v ** 2)) * t2

    d1 = (math.log(fs / i1) + bgamma_t1) / vsqrt_t1
    d3 = (math.log(fs / i1) - bgamma_t1) / vsqrt_t1

    d2 = (math.log((i2 ** 2) / (fs * i1)) + bgamma_t1) / vsqrt_t1
    d4 = (math.log((i2 ** 2) / (fs * i1)) - bgamma_t1) / vsqrt_t1

    e1 = (math.log(fs / h) + bgamma_t2) / vsqrt_t2
    e2 = (math.log((i2 ** 2) / (fs * h)) + bgamma_t2) / vsqrt_t2
    e3 = (math.log((i1 ** 2) / (fs * h)) + bgamma_t2) / vsqrt_t2
    e4 = (math.log((fs * (i1 ** 2)) / (h * (i2 ** 2))) + bgamma_t2) / vsqrt_t2

    tau = math.sqrt(t1 / t2)
    lambda1 = (-r + gamma * b + 0.5 * gamma * (gamma - 1) * (v ** 2))
    kappa = (2 * b) / (v ** 2) + (2 * gamma - 1)

    psi = math.exp(lambda1 * t2) * (fs ** gamma) * (_cbnd(-d1, -e1, tau)
                                                    - ((i2 / fs) ** kappa) * _cbnd(-d2, -e2, tau)
                                                    - ((i1 / fs) ** kappa) * _cbnd(-d3, -e3, -tau)
                                                    + ((i1 / i2) ** kappa) * _cbnd(-d4, -e4, -tau))
    return psi


# %%
# -----------
# The Phi() function used by _Bjerksund_Stensland_2002 model and the _Bjerksund_Stensland_1993 model
def _phi(fs, t, gamma, h, i, r, b, v):
    d1 = -(math.log(fs / h) + (b + (gamma - 0.5) * (v ** 2)) * t) / (v * math.sqrt(t))
    d2 = d1 - 2 * math.log(i / fs) / (v * math.sqrt(t))

    lambda1 = (-r + gamma * b + 0.5 * gamma * (gamma - 1) * (v ** 2))
    kappa = (2 * b) / (v ** 2) + (2 * gamma - 1)

    phi = math.exp(lambda1 * t) * (fs ** gamma) * (norm.cdf(d1) - ((i / fs) ** kappa) * norm.cdf(d2))

    _debug("-----")
    _debug("Debug info for: _phi()")
    _debug("    d1={0}".format(d1))
    _debug("    d2={0}".format(d2))
    _debug("    lambda={0}".format(lambda1))
    _debug("    kappa={0}".format(kappa))
    _debug("    phi={0}".format(phi))
    return phi


# %%
# -----------
# Cumulative Bivariate Normal Distribution
# Primarily called by Psi() function, part of the _Bjerksund_Stensland_2002 model
def _cbnd(a, b, rho):
    # This distribution uses the Genz multi-variate normal distribution 
    # code found as part of the standard SciPy distribution
    lower = np.array([0, 0])
    upper = np.array([a, b])
    infin = np.array([0, 0])
    correl = rho
    error, value, inform = mvn.mvndst(lower, upper, infin, correl)
    return value

# %% [markdown]
# ### Implementation: Implied Vol
# This section implements implied volatility calculations. It contains 3 main models:
# 1. **At-the-Money approximation.** This is a very fast approximation for implied volatility. It is used to estimate a starting point for the search functions.
# 2. **Newton-Raphson Search.** This is a fast implied volatility search that can be used when there is a reliable estimate of Vega (i.e., European options) 
# 3. **Bisection Search.** An implied volatility search (not quite as fast as a Newton search) that can be used where there is no reliable Vega estimate (i.e., American options).
# 

# %%
# ----------
# Inputs (not all functions use all inputs)
#      fs = forward/spot price
#      x = Strike
#      t = Time (in years)
#      r = risk free rate
#      b = cost of carry
#      cp = Call or Put price
#      precision = (optional) precision at stopping point
#      max_steps = (optional) maximum number of steps

# ----------
# Approximate Implied Volatility
#
# This function is used to choose a starting point for the
# search functions (Newton and bisection searches). 
# Brenner & Subrahmanyam (1988), Feinstein (1988)

def _approx_implied_vol(option_type, fs, x, t, r, b, cp):
    _test_option_type(option_type)

    ebrt = math.exp((b - r) * t)
    ert = math.exp(-r * t)

    a = math.sqrt(2 * math.pi) / (fs * ebrt + x * ert)

    if option_type == "c":
        payoff = fs * ebrt - x * ert
    else:
        payoff = x * ert - fs * ebrt

    b = cp - payoff / 2
    c = (payoff ** 2) / math.pi

    v = (a * (b + math.sqrt(b ** 2 + c))) / math.sqrt(t)

    return v


# %%
# ----------
# Find the Implied Volatility of an European (GBS) Option given a price
# using Newton-Raphson method for greater speed since Vega is available

def _gbs_implied_vol(option_type, fs, x, t, r, b, cp, precision=.00001, max_steps=100):
    return _newton_implied_vol(_gbs, option_type, x, fs, t, b, r, cp, precision, max_steps)


# %%
# ----------
# Find the Implied Volatility of an American Option given a price
# Using bisection method since Vega is difficult to estimate for Americans
def _american_implied_vol(option_type, fs, x, t, r, b, cp, precision=.00001, max_steps=100):
    return _bisection_implied_vol(_american_option, option_type, fs, x, t, r, b, cp, precision, max_steps)


# %%
# ----------
# Calculate Implied Volatility with a Newton Raphson search
def _newton_implied_vol(val_fn, option_type, x, fs, t, b, r, cp, precision=.00001, max_steps=100):
    # make sure a valid option type was entered
    _test_option_type(option_type)

    # Estimate starting Vol, making sure it is allowable range
    v = _approx_implied_vol(option_type, fs, x, t, r, b, cp)
    v = max(_GBS_Limits.MIN_V, v)
    v = min(_GBS_Limits.MAX_V, v)

    # Calculate the value at the estimated vol
    value, delta, gamma, theta, vega, rho = val_fn(option_type, fs, x, t, r, b, v)
    min_diff = abs(cp - value)

    _debug("-----")
    _debug("Debug info for: _Newton_ImpliedVol()")
    _debug("    Vinitial={0}".format(v))

    # Newton-Raphson Search
    countr = 0
    while precision <= abs(cp - value) <= min_diff and countr < max_steps:

        v = v - (value - cp) / vega
        if (v > _GBS_Limits.MAX_V) or (v < _GBS_Limits.MIN_V):
            _debug("    Volatility out of bounds")
            break

        value, delta, gamma, theta, vega, rho = val_fn(option_type, fs, x, t, r, b, v)
        min_diff = min(abs(cp - value), min_diff)

        # keep track of how many loops
        countr += 1
        _debug("     IVOL STEP {0}. v={1}".format(countr, v))

    
    # check if function converged and return a value
    if abs(cp - value) < precision:
        # the search function converged
        return v
    else:
        # if the search function didn't converge, try a bisection search
        return _bisection_implied_vol(val_fn, option_type, fs, x, t, r, b, cp, precision, max_steps)


# %%
# ----------
# Find the Implied Volatility using a Bisection search
def _bisection_implied_vol(val_fn, option_type, fs, x, t, r, b, cp, precision=.00001, max_steps=100):
    _debug("-----")
    _debug("Debug info for: _bisection_implied_vol()")

    # Estimate Upper and Lower bounds on volatility
    # Assume American Implied vol is within +/- 50% of the GBS Implied Vol
    v_mid = _approx_implied_vol(option_type, fs, x, t, r, b, cp)

    if (v_mid <= _GBS_Limits.MIN_V) or (v_mid >= _GBS_Limits.MAX_V):
        # if the volatility estimate is out of bounds, search entire allowed vol space
        v_low = _GBS_Limits.MIN_V
        v_high = _GBS_Limits.MAX_V
        v_mid = (v_low + v_high) / 2
    else:
        # reduce the size of the vol space
        v_low = max(_GBS_Limits.MIN_V, v_mid * .5)
        v_high = min(_GBS_Limits.MAX_V, v_mid * 1.5)

    # Estimate the high/low bounds on price
    cp_mid = val_fn(option_type, fs, x, t, r, b, v_mid)[0]
    
    # initialize bisection loop
    current_step = 0
    diff = abs(cp - cp_mid)

    _debug("     American IVOL starting conditions: CP={0} cp_mid={1}".format(cp, cp_mid))
    _debug("     IVOL {0}. V[{1},{2},{3}]".format(current_step, v_low, v_mid, v_high))

    # Keep bisection volatility until correct price is found
    while (diff > precision) and (current_step < max_steps):
        current_step += 1

        # Cut the search area in half
        if cp_mid < cp:
            v_low = v_mid
        else:
            v_high = v_mid

        cp_low = val_fn(option_type, fs, x, t, r, b, v_low)[0]
        cp_high = val_fn(option_type, fs, x, t, r, b, v_high)[0]

        v_mid = v_low + (cp - cp_low) * (v_high - v_low) / (cp_high - cp_low)
        v_mid = max(_GBS_Limits.MIN_V, v_mid)  # enforce high/low bounds
        v_mid = min(_GBS_Limits.MAX_V, v_mid)  # enforce high/low bounds

        cp_mid = val_fn(option_type, fs, x, t, r, b, v_mid)[0]
        diff = abs(cp - cp_mid)

        _debug("     IVOL {0}. V[{1},{2},{3}]".format(current_step, v_low, v_mid, v_high))

    # return output
    if abs(cp - cp_mid) < precision:
        return v_mid
    else:
        raise GBS_CalculationError(
            "Implied Vol did not converge. Best Guess={0}, Price diff={1}, Required Precision={2}".format(v_mid, diff,
                                                                                                          precision))

# %% [markdown]
# --------------------
# ### Public Interface for valuation functions
# This section encapsulates the functions that user will call to value certain options. These function primarily figure out the cost-of-carry term (b) and then call the generic version of the function (like _GBS() or _American). All of these functions return an array containg the premium and the greeks.
# 

# %%
# This is the public interface for European Options
# Each call does a little bit of processing and then calls the calculations located in the _gbs module

# Inputs: 
#    option_type = "p" or "c"
#    fs          = price of underlying
#    x           = strike
#    t           = time to expiration
#    v           = implied volatility
#    r           = risk free rate
#    q           = dividend payment
#    b           = cost of carry
# Outputs: 
#    value       = price of the option
#    delta       = first derivative of value with respect to price of underlying
#    gamma       = second derivative of value w.r.t price of underlying
#    theta       = first derivative of value w.r.t. time to expiration
#    vega        = first derivative of value w.r.t. implied volatility
#    rho         = first derivative of value w.r.t. risk free rates


# %%
# ---------------------------
# Black Scholes: stock Options (no dividend yield)
def black_scholes(option_type, fs, x, t, r, v):
    b = r
    return _gbs(option_type, fs, x, t, r, b, v)


# %%
# ---------------------------
# Merton Model: Stocks Index, stocks with a continuous dividend yields
def merton(option_type, fs, x, t, r, q, v):
    b = r - q
    return _gbs(option_type, fs, x, t, r, b, v)


# %%
# ---------------------------
# Commodities
def black_76(option_type, fs, x, t, r, v):
    b = 0
    return _gbs(option_type, fs, x, t, r, b, v)


# %%
# ---------------------------
# FX Options
def garman_kohlhagen(option_type, fs, x, t, r, rf, v):
    b = r - rf
    return _gbs(option_type, fs, x, t, r, b, v)


# %%
# ---------------------------
# Average Price option on commodities
def asian_76(option_type, fs, x, t, t_a, r, v):
    # Check that TA is reasonable
    if (t_a < _GBS_Limits.MIN_TA) or (t_a > t):
        raise GBS_InputError(
            "Invalid Input Averaging Time (TA = {0}). Acceptable range for inputs is {1} to <T".format(t_a,
                                                                                                       _GBS_Limits.MIN_TA))

    # Approximation to value Asian options on commodities
    b = 0
    if t_a == t:
        # if there is no averaging period, this is just Black Scholes
        v_a = v
    else:
        # Approximate the volatility
        m = (2 * math.exp((v ** 2) * t) - 2 * math.exp((v ** 2) * t_a) * (1 + (v ** 2) * (t - t_a))) / (
            (v ** 4) * ((t - t_a) ** 2))
        v_a = math.sqrt(math.log(m) / t)

    # Finally, have the GBS function do the calculation
    return _gbs(option_type, fs, x, t, r, b, v_a)


# %%
# ---------------------------
# Spread Option formula
def kirks_76(option_type, f1, f2, x, t, r, v1, v2, corr):
    # create the modifications to the GBS formula to handle spread options
    b = 0
    fs = f1 / (f2 + x)
    f_temp = f2 / (f2 + x)
    v = math.sqrt((v1 ** 2) + ((v2 * f_temp) ** 2) - (2 * corr * v1 * v2 * f_temp))
    my_values = _gbs(option_type, fs, 1.0, t, r, b, v)

    # Have the GBS function return a value
    return my_values[0] * (f2 + x), 0, 0, 0, 0, 0


# %%
# ---------------------------
# American Options (stock style, set q=0 for non-dividend paying options)
def american(option_type, fs, x, t, r, q, v):
    b = r - q
    return _american_option(option_type, fs, x, t, r, b, v)


# %%
# ---------------------------
# Commodities
def american_76(option_type, fs, x, t, r, v):
    b = 0
    return _american_option(option_type, fs, x, t, r, b, v)

# %% [markdown]
# ### Public Interface for implied Volatility Functions

# %%
# Inputs: 
#    option_type = "p" or "c"
#    fs          = price of underlying
#    x           = strike
#    t           = time to expiration
#    v           = implied volatility
#    r           = risk free rate
#    q           = dividend payment
#    b           = cost of carry
# Outputs: 
#    value       = price of the option
#    delta       = first derivative of value with respect to price of underlying
#    gamma       = second derivative of value w.r.t price of underlying
#    theta       = first derivative of value w.r.t. time to expiration
#    vega        = first derivative of value w.r.t. implied volatility
#    rho         = first derivative of value w.r.t. risk free rates


# %%
def euro_implied_vol(option_type, fs, x, t, r, q, cp):
    b = r - q
    return _gbs_implied_vol(option_type, fs, x, t, r, b, cp)


# %%
def euro_implied_vol_76(option_type, fs, x, t, r, cp):
    b = 0
    return _gbs_implied_vol(option_type, fs, x, t, r, b, cp)


# %%
def amer_implied_vol(option_type, fs, x, t, r, q, cp):
    b = r - q
    return _american_implied_vol(option_type, fs, x, t, r, b, cp)


# %%
def amer_implied_vol_76(option_type, fs, x, t, r, cp):
    b = 0
    return _american_implied_vol(option_type, fs, x, t, r, b, cp)

# %% [markdown]
# ### Implementation: Helper Functions
# These functions aren't part of the main code but serve as utility function mostly used for debugging

# %%
# ---------------------------
# Helper Function for Debugging

# Prints a message if running code from this module and _DEBUG is set to true
# otherwise, do nothing

def _debug(debug_input):
    if (__name__ is "__main__") and (_DEBUG is True):
        print(debug_input)


# %%
# This class defines the Exception that gets thrown when invalid input is placed into the GBS function
class GBS_InputError(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)


# %%
# This class defines the Exception that gets thrown when there is a calculation error
class GBS_CalculationError(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)


# %%
# This function tests that two floating point numbers are the same
# Numbers less than 1 million are considered the same if they are within .000001 of each other
# Numbers larger than 1 million are considered the same if they are within .0001% of each other
# User can override the default precision if necessary
def assert_close(value_a, value_b, precision=.000001):
    my_precision = precision

    if (value_a < 1000000.0) and (value_b < 1000000.0):
        my_diff = abs(value_a - value_b)
        my_diff_type = "Difference"
    else:
        my_diff = abs((value_a - value_b) / value_a)
        my_diff_type = "Percent Difference"

    _debug("Comparing {0} and {1}. Difference is {2}, Difference Type is {3}".format(value_a, value_b, my_diff,
                                                                                     my_diff_type))

    if my_diff < my_precision:
        my_result = True
    else:
        my_result = False

    if (__name__ is "__main__") and (my_result is False):
        print("  FAILED TEST. Comparing {0} and {1}. Difference is {2}, Difference Type is {3}".format(value_a, value_b,
                                                                                                       my_diff,
                                                                                                       my_diff_type))
    else:
        print(".")

    return my_result

# %% [markdown]
# 
# ## Unit Testing
# This will print out a "." if the test is successful or an error message if the test fails

# %%
if __name__ == "__main__":
    
    print ("=====================================")
    print ("American Options Intermediate Functions")
    print ("=====================================")
    
    # ---------------------------
    # unit tests for _psi()
    # _psi(FS, t2, gamma, H, I2, I1, t1, r, b, V):
    print("Testing _psi (American Option Intermediate Calculation)")
    assert_close(_psi(fs=120, t2=3, gamma=1, h=375, i2=375, i1=300, t1=1, r=.05, b=0.03, v=0.1), 112.87159814023171)
    assert_close(_psi(fs=125, t2=2, gamma=1, h=100, i2=100, i1=75, t1=1, r=.05, b=0.03, v=0.1), 1.7805459905819128)

    # ---------------------------
    # unit tests for _phi()
    print("Testing _phi (American Option Intermediate Calculation)")
    # _phi(FS, T, gamma, h, I, r, b, V):
    assert_close(_phi(fs=120, t=3, gamma=4.51339343051624, h=151.696096685711, i=151.696096685711, r=.02, b=-0.03, v=0.14),
                1102886677.05955)
    assert_close(_phi(fs=125, t=3, gamma=1, h=374.061664206768, i=374.061664206768, r=.05, b=0.03, v=0.14),
                 117.714544103477)

    # ---------------------------
    # unit tests for _CBND
    print("Testing _CBND (Cumulative Binomial Normal Distribution)")
    assert_close(_cbnd(0, 0, 0), 0.25)
    assert_close(_cbnd(0, 0, -0.5), 0.16666666666666669)
    assert_close(_cbnd(-0.5, 0, 0), 0.15426876936299347)
    assert_close(_cbnd(0, -0.5, 0), 0.15426876936299347)
    assert_close(_cbnd(0, -0.99999999, -0.99999999), 0.0)
    assert_close(_cbnd(0.000001, -0.99999999, -0.99999999), 0.0)

    assert_close(_cbnd(0, 0, 0.5), 0.3333333333333333)
    assert_close(_cbnd(0.5, 0, 0), 0.3457312306370065)
    assert_close(_cbnd(0, 0.5, 0), 0.3457312306370065)
    assert_close(_cbnd(0, 0.99999999, 0.99999999), 0.5)
    assert_close(_cbnd(0.000001, 0.99999999, 0.99999999), 0.5000003989422803)


# %%
# ---------------------------
# Testing American Options
if __name__ == "__main__":
    print("=====================================")
    print("American Options Testing")
    print("=====================================")

    print("testing _Bjerksund_Stensland_2002()")
    # _american_option(option_type, X, FS, T, b, r, V)
    assert_close(_bjerksund_stensland_2002(fs=90, x=100, t=0.5, r=0.1, b=0, v=0.15)[0], 0.8099, precision=.001)
    assert_close(_bjerksund_stensland_2002(fs=100, x=100, t=0.5, r=0.1, b=0, v=0.25)[0], 6.7661, precision=.001)
    assert_close(_bjerksund_stensland_2002(fs=110, x=100, t=0.5, r=0.1, b=0, v=0.35)[0], 15.5137, precision=.001)

    assert_close(_bjerksund_stensland_2002(fs=100, x=90, t=0.5, r=.1, b=0, v=0.15)[0], 10.5400, precision=.001)
    assert_close(_bjerksund_stensland_2002(fs=100, x=100, t=0.5, r=.1, b=0, v=0.25)[0], 6.7661, precision=.001)
    assert_close(_bjerksund_stensland_2002(fs=100, x=110, t=0.5, r=.1, b=0, v=0.35)[0], 5.8374, precision=.001)

    print("testing _Bjerksund_Stensland_1993()")
    # Prices for 1993 model slightly different than those presented in Haug's Complete Guide to Option Pricing Formulas
    # Possibly due to those results being based on older CBND calculation?
    assert_close(_bjerksund_stensland_1993(fs=90, x=100, t=0.5, r=0.1, b=0, v=0.15)[0], 0.8089, precision=.001)
    assert_close(_bjerksund_stensland_1993(fs=100, x=100, t=0.5, r=0.1, b=0, v=0.25)[0], 6.757, precision=.001)
    assert_close(_bjerksund_stensland_1993(fs=110, x=100, t=0.5, r=0.1, b=0, v=0.35)[0], 15.4998, precision=.001)

    print("testing _american_option()")
    assert_close(_american_option("p", fs=90, x=100, t=0.5, r=0.1, b=0, v=0.15)[0], 10.5400, precision=.001)
    assert_close(_american_option("p", fs=100, x=100, t=0.5, r=0.1, b=0, v=0.25)[0], 6.7661, precision=.001)
    assert_close(_american_option("p", fs=110, x=100, t=0.5, r=0.1, b=0, v=0.35)[0], 5.8374, precision=.001)

    assert_close(_american_option('c', fs=100, x=95, t=0.00273972602739726, r=0.000751040922831883, b=0, v=0.2)[0], 5.0,
                 precision=.01)
    assert_close(_american_option('c', fs=42, x=40, t=0.75, r=0.04, b=-0.04, v=0.35)[0], 5.28, precision=.01)
    assert_close(_american_option('c', fs=90, x=100, t=0.1, r=0.10, b=0, v=0.15)[0], 0.02, precision=.01)

    print("Testing that American valuation works for integer inputs")
    assert_close(_american_option('c', fs=100, x=100, t=1, r=0, b=0, v=0.35)[0], 13.892, precision=.001)
    assert_close(_american_option('p', fs=100, x=100, t=1, r=0, b=0, v=0.35)[0], 13.892, precision=.001)

    print("Testing valuation works at minimum/maximum values for T")
    assert_close(_american_option('c', 100, 100, 0.00396825396825397, 0.000771332656950173, 0, 0.15)[0], 0.3769,
                 precision=.001)
    assert_close(_american_option('p', 100, 100, 0.00396825396825397, 0.000771332656950173, 0, 0.15)[0], 0.3769,
                 precision=.001)
    assert_close(_american_option('c', 100, 100, 100, 0.042033868311581, 0, 0.15)[0], 18.61206, precision=.001)
    assert_close(_american_option('p', 100, 100, 100, 0.042033868311581, 0, 0.15)[0], 18.61206, precision=.001)

    print("Testing valuation works at minimum/maximum values for X")
    assert_close(_american_option('c', 100, 0.01, 1, 0.00330252458693489, 0, 0.15)[0], 99.99, precision=.001)
    assert_close(_american_option('p', 100, 0.01, 1, 0.00330252458693489, 0, 0.15)[0], 0, precision=.001)
    assert_close(_american_option('c', 100, 2147483248, 1, 0.00330252458693489, 0, 0.15)[0], 0, precision=.001)
    assert_close(_american_option('p', 100, 2147483248, 1, 0.00330252458693489, 0, 0.15)[0], 2147483148, precision=.001)

    print("Testing valuation works at minimum/maximum values for F/S")
    assert_close(_american_option('c', 0.01, 100, 1, 0.00330252458693489, 0, 0.15)[0], 0, precision=.001)
    assert_close(_american_option('p', 0.01, 100, 1, 0.00330252458693489, 0, 0.15)[0], 99.99, precision=.001)
    assert_close(_american_option('c', 2147483248, 100, 1, 0.00330252458693489, 0, 0.15)[0], 2147483148, precision=.001)
    assert_close(_american_option('p', 2147483248, 100, 1, 0.00330252458693489, 0, 0.15)[0], 0, precision=.001)

    print("Testing valuation works at minimum/maximum values for b")
    assert_close(_american_option('c', 100, 100, 1, 0, -1, 0.15)[0], 0.0, precision=.001)
    assert_close(_american_option('p', 100, 100, 1, 0, -1, 0.15)[0], 63.2121, precision=.001)
    assert_close(_american_option('c', 100, 100, 1, 0, 1, 0.15)[0], 171.8282, precision=.001)
    assert_close(_american_option('p', 100, 100, 1, 0, 1, 0.15)[0], 0.0, precision=.001)

    print("Testing valuation works at minimum/maximum values for r")
    assert_close(_american_option('c', 100, 100, 1, -1, 0, 0.15)[0], 16.25133, precision=.001)
    assert_close(_american_option('p', 100, 100, 1, -1, 0, 0.15)[0], 16.25133, precision=.001)
    assert_close(_american_option('c', 100, 100, 1, 1, 0, 0.15)[0], 3.6014, precision=.001)
    assert_close(_american_option('p', 100, 100, 1, 1, 0, 0.15)[0], 3.6014, precision=.001)

    print("Testing valuation works at minimum/maximum values for V")
    assert_close(_american_option('c', 100, 100, 1, 0.05, 0, 0.005)[0], 0.1916, precision=.001)
    assert_close(_american_option('p', 100, 100, 1, 0.05, 0, 0.005)[0], 0.1916, precision=.001)
    assert_close(_american_option('c', 100, 100, 1, 0.05, 0, 1)[0], 36.4860, precision=.001)
    assert_close(_american_option('p', 100, 100, 1, 0.05, 0, 1)[0], 36.4860, precision=.001)


# %%
# ---------------------------
# Testing European Options
if __name__ == "__main__":
    print("=====================================")
    print("Generalized Black Scholes (GBS) Testing")
    print("=====================================")

    print("testing GBS Premium")
    assert_close(_gbs('c', 100, 95, 0.00273972602739726, 0.000751040922831883, 0, 0.2)[0], 4.99998980469552)
    assert_close(_gbs('c', 92.45, 107.5, 0.0876712328767123, 0.00192960198828152, 0, 0.3)[0], 0.162619795863781)
    assert_close(_gbs('c', 93.0766666666667, 107.75, 0.164383561643836, 0.00266390125346286, 0, 0.2878)[0],
                 0.584588840095316)
    assert_close(_gbs('c', 93.5333333333333, 107.75, 0.249315068493151, 0.00319934651984034, 0, 0.2907)[0],
                 1.27026849732877)
    assert_close(_gbs('c', 93.8733333333333, 107.75, 0.331506849315069, 0.00350934592318849, 0, 0.2929)[0],
                 1.97015685523537)
    assert_close(_gbs('c', 94.1166666666667, 107.75, 0.416438356164384, 0.00367360967852615, 0, 0.2919)[0],
                 2.61731599547608)
    assert_close(_gbs('p', 94.2666666666667, 107.75, 0.498630136986301, 0.00372609838856132, 0, 0.2888)[0],
                 16.6074587545269)
    assert_close(_gbs('p', 94.3666666666667, 107.75, 0.583561643835616, 0.00370681407974257, 0, 0.2923)[0],
                 17.1686196701434)
    assert_close(_gbs('p', 94.44, 107.75, 0.668493150684932, 0.00364163303865433, 0, 0.2908)[0], 17.6038273793172)
    assert_close(_gbs('p', 94.4933333333333, 107.75, 0.750684931506849, 0.00355604221290591, 0, 0.2919)[0],
                 18.0870982577296)
    assert_close(_gbs('p', 94.49, 107.75, 0.835616438356164, 0.00346100468320478, 0, 0.2901)[0], 18.5149895730975)
    assert_close(_gbs('p', 94.39, 107.75, 0.917808219178082, 0.00337464630758452, 0, 0.2876)[0], 18.9397688539483)

    print("Testing that valuation works for integer inputs")
    assert_close(_gbs('c', fs=100, x=95, t=1, r=1, b=0, v=1)[0], 14.6711476484)
    assert_close(_gbs('p', fs=100, x=95, t=1, r=1, b=0, v=1)[0], 12.8317504425)

    print("Testing valuation works at minimum/maximum values for T")
    assert_close(_gbs('c', 100, 100, 0.00396825396825397, 0.000771332656950173, 0, 0.15)[0], 0.376962465712609)
    assert_close(_gbs('p', 100, 100, 0.00396825396825397, 0.000771332656950173, 0, 0.15)[0], 0.376962465712609)
    assert_close(_gbs('c', 100, 100, 100, 0.042033868311581, 0, 0.15)[0], 0.817104022604705)
    assert_close(_gbs('p', 100, 100, 100, 0.042033868311581, 0, 0.15)[0], 0.817104022604705)

    print("Testing valuation works at minimum/maximum values for X")
    assert_close(_gbs('c', 100, 0.01, 1, 0.00330252458693489, 0, 0.15)[0], 99.660325245681)
    assert_close(_gbs('p', 100, 0.01, 1, 0.00330252458693489, 0, 0.15)[0], 0)
    assert_close(_gbs('c', 100, 2147483248, 1, 0.00330252458693489, 0, 0.15)[0], 0)
    assert_close(_gbs('p', 100, 2147483248, 1, 0.00330252458693489, 0, 0.15)[0], 2140402730.16601)

    print("Testing valuation works at minimum/maximum values for F/S")
    assert_close(_gbs('c', 0.01, 100, 1, 0.00330252458693489, 0, 0.15)[0], 0)
    assert_close(_gbs('p', 0.01, 100, 1, 0.00330252458693489, 0, 0.15)[0], 99.660325245681)
    assert_close(_gbs('c', 2147483248, 100, 1, 0.00330252458693489, 0, 0.15)[0], 2140402730.16601)
    assert_close(_gbs('p', 2147483248, 100, 1, 0.00330252458693489, 0, 0.15)[0], 0)

    print("Testing valuation works at minimum/maximum values for b")
    assert_close(_gbs('c', 100, 100, 1, 0.05, -1, 0.15)[0], 1.62505648981223E-11)
    assert_close(_gbs('p', 100, 100, 1, 0.05, -1, 0.15)[0], 60.1291675389721)
    assert_close(_gbs('c', 100, 100, 1, 0.05, 1, 0.15)[0], 163.448023481557)
    assert_close(_gbs('p', 100, 100, 1, 0.05, 1, 0.15)[0], 4.4173615264761E-11)

    print("Testing valuation works at minimum/maximum values for r")
    assert_close(_gbs('c', 100, 100, 1, -1, 0, 0.15)[0], 16.2513262267156)
    assert_close(_gbs('p', 100, 100, 1, -1, 0, 0.15)[0], 16.2513262267156)
    assert_close(_gbs('c', 100, 100, 1, 1, 0, 0.15)[0], 2.19937783786316)
    assert_close(_gbs('p', 100, 100, 1, 1, 0, 0.15)[0], 2.19937783786316)

    print("Testing valuation works at minimum/maximum values for V")
    assert_close(_gbs('c', 100, 100, 1, 0.05, 0, 0.005)[0], 0.189742620249)
    assert_close(_gbs('p', 100, 100, 1, 0.05, 0, 0.005)[0], 0.189742620249)

    assert_close(_gbs('c', 100, 100, 1, 0.05, 0, 1)[0], 36.424945370234)
    assert_close(_gbs('p', 100, 100, 1, 0.05, 0, 1)[0], 36.424945370234)

    print("Checking that Greeks work for calls")
    assert_close(_gbs('c', 100, 100, 1, 0.05, 0, 0.15)[0], 5.68695251984796)
    assert_close(_gbs('c', 100, 100, 1, 0.05, 0, 0.15)[1], 0.50404947485)
    assert_close(_gbs('c', 100, 100, 1, 0.05, 0, 0.15)[2], 0.025227988795588)
    assert_close(_gbs('c', 100, 100, 1, 0.05, 0, 0.15)[3], -2.55380111351125)
    assert_close(_gbs('c', 100, 100, 2, 0.05, 0.05, 0.25)[4], 50.7636345571413)
    assert_close(_gbs('c', 100, 100, 1, 0.05, 0, 0.15)[5], 44.7179949651117)

    print("Checking that Greeks work for puts")
    assert_close(_gbs('p', 100, 100, 1, 0.05, 0, 0.15)[0], 5.68695251984796)
    assert_close(_gbs('p', 100, 100, 1, 0.05, 0, 0.15)[1], -0.447179949651)
    assert_close(_gbs('p', 100, 100, 1, 0.05, 0, 0.15)[2], 0.025227988795588)
    assert_close(_gbs('p', 100, 100, 1, 0.05, 0, 0.15)[3], -2.55380111351125)
    assert_close(_gbs('p', 100, 100, 2, 0.05, 0.05, 0.25)[4], 50.7636345571413)
    assert_close(_gbs('p', 100, 100, 1, 0.05, 0, 0.15)[5], -50.4049474849597)


# %%
# ---------------------------
# Testing Implied Volatility
if __name__ == "__main__":
    print("=====================================")
    print("Implied Volatility Testing")
    print("=====================================")
    print("For options far away from ATM or those very near to expiry, volatility")
    print("doesn't have a major effect on the price. When large changes in vol result in")
    print("price changes less than the minimum precision, it is very difficult to test implied vol")
    print("=====================================")

    print ("testing at-the-money approximation")
    assert_close(_approx_implied_vol(option_type="c", fs=100, x=100, t=1, r=.05, b=0, cp=5),0.131757)
    assert_close(_approx_implied_vol(option_type="c", fs=59, x=60, t=0.25, r=.067, b=0.067, cp=2.82),0.239753)

    print("testing GBS Implied Vol")
    assert_close(_gbs_implied_vol('c', 92.45, 107.5, 0.0876712328767123, 0.00192960198828152, 0, 0.162619795863781),0.3)
    assert_close(_gbs_implied_vol('c', 93.0766666666667, 107.75, 0.164383561643836, 0.00266390125346286, 0, 0.584588840095316),0.2878)
    assert_close(_gbs_implied_vol('c', 93.5333333333333, 107.75, 0.249315068493151, 0.00319934651984034, 0, 1.27026849732877),0.2907)
    assert_close(_gbs_implied_vol('c', 93.8733333333333, 107.75, 0.331506849315069, 0.00350934592318849, 0, 1.97015685523537),0.2929)
    assert_close(_gbs_implied_vol('c', 94.1166666666667, 107.75, 0.416438356164384, 0.00367360967852615, 0, 2.61731599547608),0.2919)
    assert_close(_gbs_implied_vol('p', 94.2666666666667, 107.75, 0.498630136986301, 0.00372609838856132, 0, 16.6074587545269),0.2888)
    assert_close(_gbs_implied_vol('p', 94.3666666666667, 107.75, 0.583561643835616, 0.00370681407974257, 0, 17.1686196701434),0.2923)
    assert_close(_gbs_implied_vol('p', 94.44, 107.75, 0.668493150684932, 0.00364163303865433, 0, 17.6038273793172),0.2908)
    assert_close(_gbs_implied_vol('p', 94.4933333333333, 107.75, 0.750684931506849, 0.00355604221290591, 0, 18.0870982577296),0.2919)
    assert_close(_gbs_implied_vol('p', 94.39, 107.75, 0.917808219178082, 0.00337464630758452, 0, 18.9397688539483),0.2876)

    print("Testing that GBS implied vol works for integer inputs")
    assert_close(_gbs_implied_vol('c', fs=100, x=95, t=1, r=1, b=0, cp=14.6711476484), 1)
    assert_close(_gbs_implied_vol('p', fs=100, x=95, t=1, r=1, b=0, cp=12.8317504425), 1)

    print("testing American Option implied volatility")
    assert_close(_american_implied_vol("p", fs=90, x=100, t=0.5, r=0.1, b=0, cp=10.54), 0.15, precision=0.01)
    assert_close(_american_implied_vol("p", fs=100, x=100, t=0.5, r=0.1, b=0, cp=6.7661), 0.25, precision=0.0001)
    assert_close(_american_implied_vol("p", fs=110, x=100, t=0.5, r=0.1, b=0, cp=5.8374), 0.35, precision=0.0001)
    assert_close(_american_implied_vol('c', fs=42, x=40, t=0.75, r=0.04, b=-0.04, cp=5.28), 0.35, precision=0.01)
    assert_close(_american_implied_vol('c', fs=90, x=100, t=0.1, r=0.10, b=0, cp=0.02), 0.15, precision=0.01)

    print("Testing that American implied volatility works for integer inputs")
    assert_close(_american_implied_vol('c', fs=100, x=100, t=1, r=0, b=0, cp=13.892), 0.35, precision=0.01)
    assert_close(_american_implied_vol('p', fs=100, x=100, t=1, r=0, b=0, cp=13.892), 0.35, precision=0.01)


# %%
# ---------------------------
# Testing the external interface
if __name__ == "__main__":
    print("=====================================")
    print("External Interface Testing")
    print("=====================================")

    # BlackScholes(option_type, X, FS, T, r, V)
    print("Testing: GBS.BlackScholes")
    assert_close(black_scholes('c', 102, 100, 2, 0.05, 0.25)[0], 20.02128028)
    assert_close(black_scholes('p', 102, 100, 2, 0.05, 0.25)[0], 8.50502208)

    # Merton(option_type, X, FS, T, r, q, V)
    print("Testing: GBS.Merton")
    assert_close(merton('c', 102, 100, 2, 0.05, 0.01, 0.25)[0], 18.63371484)
    assert_close(merton('p', 102, 100, 2, 0.05, 0.01, 0.25)[0], 9.13719197)

    # Black76(option_type, X, FS, T, r, V)
    print("Testing: GBS.Black76")
    assert_close(black_76('c', 102, 100, 2, 0.05, 0.25)[0], 13.74803567)
    assert_close(black_76('p', 102, 100, 2, 0.05, 0.25)[0], 11.93836083)

    # garman_kohlhagen(option_type, X, FS, T, b, r, rf, V)
    print("Testing: GBS.garman_kohlhagen")
    assert_close(garman_kohlhagen('c', 102, 100, 2, 0.05, 0.01, 0.25)[0], 18.63371484)
    assert_close(garman_kohlhagen('p', 102, 100, 2, 0.05, 0.01, 0.25)[0], 9.13719197)

    # Asian76(option_type, X, FS, T, TA, r, V):
    print("Testing: Asian76")
    assert_close(asian_76('c', 102, 100, 2, 1.9, 0.05, 0.25)[0], 13.53508930)
    assert_close(asian_76('p', 102, 100, 2, 1.9, 0.05, 0.25)[0], 11.72541446)

    # Kirks76(option_type, X, F1, F2, T, r, V1, V2, corr)
    print("Testing: Kirks")
    assert_close(kirks_76("c", f1=37.384913362, f2=42.1774, x=3.0, t=0.043055556, r=0, v1=0.608063, v2=0.608063, corr=.8)[0],0.007649192)
    assert_close(kirks_76("p", f1=37.384913362, f2=42.1774, x=3.0, t=0.043055556, r=0, v1=0.608063, v2=0.608063, corr=.8)[0],7.80013583)


# %%
# ---------------------------
# Testing the external interface
if __name__ == "__main__":
    print("=====================================")
    print("External Interface Testing")
    print("=====================================")

    # BlackScholes(option_type, X, FS, T, r, V)
    print("Testing: GBS.BlackScholes")
    assert_close(black_scholes('c', 102, 100, 2, 0.05, 0.25)[0], 20.02128028)
    assert_close(black_scholes('p', 102, 100, 2, 0.05, 0.25)[0], 8.50502208)

    # Merton(option_type, X, FS, T, r, q, V)
    print("Testing: GBS.Merton")
    assert_close(merton('c', 102, 100, 2, 0.05, 0.01, 0.25)[0], 18.63371484)
    assert_close(merton('p', 102, 100, 2, 0.05, 0.01, 0.25)[0], 9.13719197)

    # Black76(option_type, X, FS, T, r, V)
    print("Testing: GBS.Black76")
    assert_close(black_76('c', 102, 100, 2, 0.05, 0.25)[0], 13.74803567)
    assert_close(black_76('p', 102, 100, 2, 0.05, 0.25)[0], 11.93836083)

    # garman_kohlhagen(option_type, X, FS, T, b, r, rf, V)
    print("Testing: GBS.garman_kohlhagen")
    assert_close(garman_kohlhagen('c', 102, 100, 2, 0.05, 0.01, 0.25)[0], 18.63371484)
    assert_close(garman_kohlhagen('p', 102, 100, 2, 0.05, 0.01, 0.25)[0], 9.13719197)

    # Asian76(option_type, X, FS, T, TA, r, V):
    print("Testing: Asian76")
    assert_close(asian_76('c', 102, 100, 2, 1.9, 0.05, 0.25)[0], 13.53508930)
    assert_close(asian_76('p', 102, 100, 2, 1.9, 0.05, 0.25)[0], 11.72541446)

    # Kirks76(option_type, X, F1, F2, T, r, V1, V2, corr)
    print("Testing: Kirks")
    assert_close(
        kirks_76("c", f1=37.384913362, f2=42.1774, x=3.0, t=0.043055556, r=0, v1=0.608063, v2=0.608063, corr=.8)[0],
        0.007649192)
    assert_close(
        kirks_76("p", f1=37.384913362, f2=42.1774, x=3.0, t=0.043055556, r=0, v1=0.608063, v2=0.608063, corr=.8)[0],
        7.80013583)

# %% [markdown]
# ## Benchmarking
# 
# This section benchmarks the output against output from a 3rd party option pricing libraries described in the book "The Complete Guide to Option Pricing Formulas" by Esper Haug.
# 
# *Haug, Esper. The Complete Guide to Option Pricing Formulas. McGraw-Hill 1997, pages 10-15*
# 
# 
# Indexes for GBS Functions:
# * [0] Value
# * [1] Delta
# * [2] Gamma
# * [3] Theta (annualized, divide by 365 to get daily theta)
# * [4] Vega
# * [5] Rho

# %%
# ------------------
# Benchmarking against other option models

if __name__ == "__main__":
    print("=====================================")
    print("Selected Comparison to 3rd party models")
    print("=====================================")

    print("Testing GBS.BlackScholes")
    assert_close(black_scholes('c', fs=60, x=65, t=0.25, r=0.08, v=0.30)[0], 2.13336844492)

    print("Testing GBS.Merton")
    assert_close(merton('p', fs=100, x=95, t=0.5, r=0.10, q=0.05, v=0.20)[0], 2.46478764676)

    print("Testing GBS.Black76")
    assert_close(black_76('c', fs=19, x=19, t=0.75, r=0.10, v=0.28)[0], 1.70105072524)

    print("Testing GBS.garman_kohlhagen")
    assert_close(garman_kohlhagen('c', fs=1.56, x=1.60, t=0.5, r=0.06, rf=0.08, v=0.12)[0], 0.0290992531494)

    print("Testing Delta")
    assert_close(black_76('c', fs=105, x=100, t=0.5, r=0.10, v=0.36)[1], 0.5946287)
    assert_close(black_76('p', fs=105, x=100, t=0.5, r=0.10, v=0.36)[1], -0.356601)

    print("Testing Gamma")
    assert_close(black_scholes('c', fs=55, x=60, t=0.75, r=0.10, v=0.30)[2], 0.0278211604769)
    assert_close(black_scholes('p', fs=55, x=60, t=0.75, r=0.10, v=0.30)[2], 0.0278211604769)

    print("Testing Theta")
    assert_close(merton('p', fs=430, x=405, t=0.0833, r=0.07, q=0.05, v=0.20)[3], -31.1923670565)

    print("Testing Vega")
    assert_close(black_scholes('c', fs=55, x=60, t=0.75, r=0.10, v=0.30)[4], 18.9357773496)
    assert_close(black_scholes('p', fs=55, x=60, t=0.75, r=0.10, v=0.30)[4], 18.9357773496)

    print("Testing Rho")
    assert_close(black_scholes('c', fs=72, x=75, t=1, r=0.09, v=0.19)[5], 38.7325050173)


# %%


