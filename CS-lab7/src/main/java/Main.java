import com.mongodb.MongoClient;
import com.mongodb.MongoCredential;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import org.bson.Document;

public class Main {
    public static void main(String[] args) {
        MongoClient mongo = new MongoClient( "localhost" , 27017 );

        MongoCredential credentials= MongoCredential.createCredential("sampleUser", "Persons", "password".toCharArray());
        System.out.println("Connected to the database successfully");

        MongoDatabase mongoDB = mongo.getDatabase("Persons");

        MongoCollection<Document> persons = mongoDB.getCollection("Persons");
        System.out.println("Collection myCollection selected successfully");

        DocumentEncrDecr doc = new DocumentEncrDecr();
        doc.encryptFields(persons);
    }
}
