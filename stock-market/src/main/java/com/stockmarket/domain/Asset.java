package com.stockmarket.domain;

import java.math.BigDecimal;

public abstract class Asset {
    private final String name;
    private final BigDecimal basePrice;

    public Asset(String name, BigDecimal basePrice) {
        this.name = name;
        this.basePrice = basePrice;
    }

    // Metoda abstrakcyjna - klucz do polimorfizmu
    public abstract BigDecimal calculateRealValue(int quantity);

    // Metoda wspólna - koszt zakupu (cena * ilość)
    // Akcje mogą to nadpisać jeśli mają opłaty wstępne
    public BigDecimal calculatePurchaseCost(int quantity) {
        return basePrice.multiply(BigDecimal.valueOf(quantity));
    }

    public String getName() {
        return name;
    }

    public BigDecimal getBasePrice() {
        return basePrice;
    }
}
