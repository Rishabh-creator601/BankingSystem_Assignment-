package flight;

import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.time.format.ResolverStyle;
import java.util.Set;


public class FlightSearch {
   private String  departureDate;
   private String  departureAirportCode;
   private boolean emergencyRowSeating;
   private String  returnDate;
   private String  destinationAirportCode; 
   private String  seatingClass;
   private int     adultPassengerCount;
   private int     childPassengerCount;
   private int     infantPassengerCount;


   private LocalDate parseStrictDate(String dateStr) {
        try {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/uuuu")
                    .withResolverStyle(ResolverStyle.STRICT);
            return LocalDate.parse(dateStr, formatter);
        } catch (DateTimeParseException e) {
            throw new IllegalArgumentException("Invalid date: " + dateStr 
                    + ". Ensure format is DD/MM/YYYY and the date is valid.");
        }
    }


   public boolean runFlightSearch(String departureDate, String departureAirportCode, boolean emergencyRowSeating, 
                               String returnDate, String destinationAirportCode, String seatingClass, 
                               int adultPassengerCount, int childPassengerCount, int infantPassengerCount) {
    
    this.departureAirportCode = departureAirportCode;
    this.departureDate = departureDate;
    this.emergencyRowSeating = emergencyRowSeating;
    this.returnDate = returnDate;
    this.destinationAirportCode = destinationAirportCode;
    this.seatingClass = seatingClass;


    Set<String> allowedAirports = Set.of("syd", "mel", "lax", "cdg", "del", "pvg", "doh");
    boolean valid= true;



    
  // 1. Passenger counts must be non-negative
        if (adultPassengerCount < 0 || childPassengerCount < 0 || infantPassengerCount < 0) {
            throw new IllegalArgumentException("Passenger counts cannot be negative.");
        }

        // Total passenger count must be 1-9
        int totalPassengers = adultPassengerCount + childPassengerCount + infantPassengerCount;
        if (totalPassengers < 1 || totalPassengers > 9) {
            throw new IllegalArgumentException("Passenger count must be in range 1-9.");
        }

        // 2. Children seating restrictions
        if (childPassengerCount > 0) {
            if (emergencyRowSeating) throw new IllegalArgumentException("Children cannot be seated in emergency row seating.");
            if ("First".equalsIgnoreCase(seatingClass)) throw new IllegalArgumentException("Children are not allowed in First Class.");
            if (childPassengerCount > 2 * adultPassengerCount)
                throw new IllegalArgumentException("Each adult can accompany up to 2 children only.");
        }

        // 3. Infants seating restrictions
        if (infantPassengerCount > 0) {
            if (emergencyRowSeating) throw new IllegalArgumentException("Infants cannot be seated in emergency row seating.");
            if ("Business".equalsIgnoreCase(seatingClass)) throw new IllegalArgumentException("Infants are not allowed in Business Class.");
            if (adultPassengerCount == 0) throw new IllegalArgumentException("Infants must be accompanied by at least one adult.");
            if (infantPassengerCount > adultPassengerCount)
                throw new IllegalArgumentException("Each infant must be seated on an adult's lap. Only one infant per adult.");
        }


        // Departure date validation
        LocalDate depDate = parseStrictDate(departureDate);
        LocalDate today = LocalDate.now();
        if (depDate.isBefore(today)) throw new IllegalArgumentException("Departure date cannot be in the past.");

        // Return date must exist and not be before departure
        if (returnDate == null || returnDate.isEmpty()) {
            throw new IllegalArgumentException("All flights are round-trip. Return date is required.");
        }
        LocalDate retDate = parseStrictDate(returnDate);
        if (retDate.isBefore(depDate)) throw new IllegalArgumentException("Return date cannot be before departure date.");

        // Seating class validation
        String seatClassLower = seatingClass.toLowerCase();
        if (!seatClassLower.equals("economy") && !seatClassLower.equals("premium economy") 
            && !seatClassLower.equals("business") && !seatClassLower.equals("first")) {
            throw new IllegalArgumentException("Seating class must be one of: economy, premium economy, business, first.");
        }

        // Emergency row seating allowed only in economy
        if (emergencyRowSeating && !seatClassLower.equals("economy")) {
            throw new IllegalArgumentException("Emergency row seating is only allowed in Economy class.");
        }

        String depCodeLower = departureAirportCode.toLowerCase();
        String destCodeLower = destinationAirportCode.toLowerCase();

        if (!allowedAirports.contains(depCodeLower)) {
            throw new IllegalArgumentException("Departure airport '" + departureAirportCode + "' is not allowed.");
        }
        if (!allowedAirports.contains(destCodeLower)) {
            throw new IllegalArgumentException("Destination airport '" + destinationAirportCode + "' is not allowed.");
        }
        if (depCodeLower.equals(destCodeLower)) {
            throw new IllegalArgumentException("Departure and destination airports cannot be the same.");
        }

        System.out.println("Booking validated successfully ✅");
        return valid;
      }


 
public static void main(String[] args) {
        FlightSearch fs = new FlightSearch();


    // 1️) Too many passengers (>9)
   // boolean valid = fs.runFlightSearch("20/10/2025","DEL",false,"28/10/2025","DOH","Economy",5,3,2);
    //boolean valid =  fs.runFlightSearch("25/10/2025","LAX",false,"05/11/2025","CDG","Economy",4,4,2);

    // 2)  Child in emergency row
// boolean valid = fs.runFlightSearch("20/10/2025","DEL",true,"28/10/2025","DOH","Economy",1,1,0);
// boolean valid =  fs.runFlightSearch("22/11/2025","SYD",true,"30/11/2025","MEL","Economy",2,1,0);

// 3️)  Child in first class
// boolean valid = fs.runFlightSearch("20/10/2025","DEL",false,"28/10/2025","DOH","First",1,1,0);
// boolean valid = fs.runFlightSearch("15/12/2025","CDG",false,"25/12/2025","LAX","First",2,2,0);

// 4️) Too many children per adult
//  boolean valid = fs.runFlightSearch("20/10/2025","DEL",false,"28/10/2025","DOH","Economy",1,3,0);
// boolean valid = fs.runFlightSearch("10/11/2025","MEL",false,"20/11/2025","PVG","Economy",1,4,0);

// // 5️) Infant in emergency row
// boolean valid = fs.runFlightSearch("20/10/2025","DEL",true,"28/10/2025","DOH","Economy",1,0,1);
// boolean valid = fs.runFlightSearch("22/11/2025","SYD",true,"30/11/2025","MEL","Economy",2,0,2);

// // 6️) Infant in business class
// boolean valid = fs.runFlightSearch("20/10/2025","DEL",false,"28/10/2025","DOH","Business",1,0,1);
// boolean valid = fs.runFlightSearch("25/12/2025","LAX",false,"05/01/2026","CDG","Business",2,0,2);

// // 7️)  Infant without adult
// boolean valid = fs.runFlightSearch("20/10/2025","DEL",false,"28/10/2025","DOH","Economy",0,0,1);
// boolean valid = fs.runFlightSearch("01/11/2025","MEL",false,"10/11/2025","PVG","Economy",0,0,2);

// // 8) Return date before departure
// boolean valid = fs.runFlightSearch("28/10/2025","DEL",false,"20/10/2025","DOH","Economy",1,0,0);
// boolean valid = fs.runFlightSearch("10/12/2025","LAX",false,"05/12/2025","CDG","Economy",2,0,0);

// // 9️) Invalid departure airport
// boolean valid = fs.runFlightSearch("20/10/2025","XYZ",false,"28/10/2025","DOH","Economy",1,0,0);
// boolean valid = fs.runFlightSearch("15/11/2025","ABC",false,"25/11/2025","MEL","Economy",1,1,0);

// // 10)  Same departure & destination
// boolean valid = fs.runFlightSearch("20/10/2025","DEL",false,"28/10/2025","DEL","Economy",1,0,0);
// boolean valid = fs.runFlightSearch("25/12/2025","LAX",false,"02/01/2026","LAX","Economy",2,1,0);

// // 11) Invalid seating class
// boolean valid = fs.runFlightSearch("20/10/2025","DEL",false,"28/10/2025","DOH","Economyy",1,0,0);
// boolean valid = fs.runFlightSearch("15/11/2025","MEL",false,"25/11/2025","PVG","Prem Economy",2,0,0);

// //  Valid input cases (4 variations)
// boolean valid = fs.runFlightSearch("20/10/2025","DEL",false,"28/10/2025","DOH","Economy",2,1,0);
// boolean valid = fs.runFlightSearch("10/11/2025","LAX",false,"20/11/2025","CDG","Premium Economy",1,0,0);
// boolean valid = fs.runFlightSearch("05/12/2025","MEL",false,"15/12/2025","PVG","Business",2,0,1);
// boolean valid = fs.runFlightSearch("01/09/2025","SYD",false,"10/09/2025","DOH","First",1,0,0);




        // System.out.println("Flight search valid: " + valid);
    }

}

