package com.stockmarket.domain;

import java.math.BigDecimal;

public class Commodity extends Asset {
    private final BigDecimal storageCostPerUnit;

    public Commodity(String name, BigDecimal basePrice, BigDecimal storageCostPerUnit) {
        super(name, basePrice);
        this.storageCostPerUnit = storageCostPerUnit;
    }

    @Override
    public BigDecimal calculateRealValue(int quantity) {
        BigDecimal rawValue = getBasePrice().multiply(BigDecimal.valueOf(quantity));
        BigDecimal storageCost = storageCostPerUnit.multiply(BigDecimal.valueOf(quantity));
        // Wartość pomniejszona o koszt magazynowania
        return rawValue.subtract(storageCost).max(BigDecimal.ZERO);
    }
}

