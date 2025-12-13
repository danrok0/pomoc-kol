package com.stockmarket.logic;

import com.stockmarket.domain.Asset;
import java.math.BigDecimal;
import java.util.HashMap;
import java.util.Map;

public class Portfolio {
    private BigDecimal cash;
    private final Map<Asset, Integer> holdings = new HashMap<>();

    public Portfolio(BigDecimal initialCash) {
        this.cash = initialCash;
    }

    public void addAsset(Asset asset, int quantity) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("Ilość musi być dodatnia");
        }

        BigDecimal cost = asset.calculatePurchaseCost(quantity);

        if (cash.compareTo(cost) < 0) {
            throw new IllegalStateException("Niewystarczające środki na zakup");
        }

        cash = cash.subtract(cost);
        holdings.merge(asset, quantity, Integer::sum);
    }

    public BigDecimal calculateTotalValue() {
        BigDecimal assetsValue = BigDecimal.ZERO;

        for (Map.Entry<Asset, Integer> entry : holdings.entrySet()) {
            Asset asset = entry.getKey();
            int quantity = entry.getValue();
            // POLIMORFIZM: Każde aktywo samo liczy swoją wartość
            assetsValue = assetsValue.add(asset.calculateRealValue(quantity));
        }

        return assetsValue.add(cash);
    }

    public BigDecimal getCash() {
        return cash;
    }
}