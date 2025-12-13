package com.stockmarket.domain;

import java.math.BigDecimal;

public class Share extends Asset {
    private static final BigDecimal HANDLING_FEE = new BigDecimal("5.00");

    public Share(String name, BigDecimal basePrice) {
        super(name, basePrice);
    }

    @Override
    public BigDecimal calculateRealValue(int quantity) {
        BigDecimal rawValue = getBasePrice().multiply(BigDecimal.valueOf(quantity));
        // Wartość to cena rynkowa pomniejszona o opłatę manipulacyjną
        return rawValue.subtract(HANDLING_FEE).max(BigDecimal.ZERO);
    }

    @Override
    public BigDecimal calculatePurchaseCost(int quantity) {
        // Przy zakupie też płacimy prowizję
        return super.calculatePurchaseCost(quantity).add(HANDLING_FEE);
    }
}