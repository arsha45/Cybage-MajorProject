import { Component } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { FriendsService } from '../friends/friends.service';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  currentUserId: number;
  users: any[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';
  currentUserName = localStorage.getItem('username')

  constructor(public authService: AuthService, private userService: FriendsService) {
    this.currentUserId = parseInt(localStorage.getItem('currentUserId') || '0');
  }

  ngOnInit(): void {
    console.log("Load user constructor");
    this.loadUsers();
  }

  

  loadUsers(): void {
    this.isLoading = true;
    
    this.userService.getUsers().subscribe(
      (data: any) => {
        this.users = data.results.map((user: any) => ({
          ...user,
          requestSent: false 
        }));
        this.isLoading = false;
      },
      (error: any) => {
        this.errorMessage = 'Error loading users. Please try again later.';
        this.isLoading = false;
      }
    );
  }

  sendFriendRequest(toUserId: number): void {
    const userIndex = this.users.findIndex(user => user.id === toUserId);
    if (userIndex !== -1 && !this.users[userIndex].requestSent) {
      this.userService.sendFriendRequest(this.currentUserId, toUserId).subscribe(
        (response: any) => {
          console.log('Friend request sent successfully', response);
          alert(`Friend request has been send`)
          this.users[userIndex].requestSent = true; 
        },
        (error: any) => {
          console.error('Error sending friend request', error);
        }
      );
    } else {
      console.log('Friend request already sent or invalid user');
    }
  }
}
