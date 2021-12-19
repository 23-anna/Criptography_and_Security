package com.cslabs.lab7.repository;

import com.cslabs.lab7.entities.UserEntity;
import org.springframework.data.repository.CrudRepository;
import org.springframework.stereotype.Repository;

@Repository("userRepository")
public interface UserRepository extends CrudRepository<UserEntity, String> {
    UserEntity findByEmailIdIgnoreCase(String emailId);
}
