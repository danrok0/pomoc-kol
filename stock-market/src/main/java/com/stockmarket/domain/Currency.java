package com.stockmarket.domain;

import java.math.BigDecimal;

public class Currency extends Asset {
    private final BigDecimal spread;

    public Currency(String name, BigDecimal basePrice, BigDecimal spread) {
        super(name, basePrice);
        this.spread = spread;
    }

    @Override
    public BigDecimal calculateRealValue(int quantity) {
        // Wartość to (Cena Rynkowa - Spread) * ilość
        BigDecimal bidPrice = getBasePrice().subtract(spread);
        return bidPrice.multiply(BigDecimal.valueOf(quantity));
    }
}