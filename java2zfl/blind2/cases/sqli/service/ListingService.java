package blind2.sqli.service;

import blind2.sqli.data.ListingRepository;
import blind2.sqli.model.ListingFilter;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Service;

@Service
public class ListingService {

    private final ListingRepository repository;

    public ListingService(ListingRepository repository) {
        this.repository = repository;
    }

    public List<Map<String, Object>> search(ListingFilter filter) {
        String sort = filter.getSortBy() == null || filter.getSortBy().isBlank() ? "listed_at DESC" : filter.getSortBy();
        int rooms = filter.getMinRooms() == null ? 0 : filter.getMinRooms();
        return repository.find(filter.getDistrict(), rooms, sort);
    }
}
