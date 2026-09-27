package blind2.sqli.service;

import blind2.sqli.data.TransferDao;
import java.util.Locale;
import org.springframework.stereotype.Service;

@Service
public class TransferService {

    private final TransferDao dao;

    public TransferService(TransferDao dao) {
        this.dao = dao;
    }

    public void transfer(String from, String to, String sku, int quantity) {
        if (quantity <= 0) {
            throw new IllegalArgumentException("quantity must be positive");
        }
        dao.recordTransfer(from.toUpperCase(Locale.ROOT), to.toUpperCase(Locale.ROOT), sku.trim(), quantity);
    }
}
