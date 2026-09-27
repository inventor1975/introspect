package blind2.sqli;

import blind2.sqli.service.TransferService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class WarehouseTransferController {

    @Autowired
    private TransferService transfers;

    @PostMapping("/api/warehouse/transfers")
    public ResponseEntity<String> transfer(@RequestParam String from, @RequestParam String to,
                                           @RequestParam String sku, @RequestParam int qty) {
        if (from.equalsIgnoreCase(to)) {
            return new ResponseEntity<>("source and target must differ", HttpStatus.BAD_REQUEST);
        }
        transfers.transfer(from, to, sku, qty);
        return ResponseEntity.ok("transfer recorded");
    }
}
