import { Component } from '@angular/core';
import { AuthService } from '../auth/auth.service';
import { FriendsService } from '../friends/friends.service';
import { PostService } from '../post/post.service';
import { ToastrService } from 'ngx-toastr';


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

  constructor( public authService: AuthService, private userService: FriendsService, private toaster: ToastrService) {
    this.currentUserId = parseInt(localStorage.getItem('currentUserId') || '0');
  }

  ngOnInit(): void {
    if (this.authService.isLoggedIn()) {
      this.currentUserId = parseInt(localStorage.getItem('currentUserId') || '0');
      this.loadUsers();
    } 
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
          this.toaster.success(`Friend request has been sent`)
          this.users[userIndex].requestSent = true; 
          this.users.splice(userIndex, 1);
        },
        (error: any) => {
          console.error('Error sending friend request', error);
          this.toaster.error('Error sending friend request', error);
        }
      );
    } else {
      console.log('Friend request already sent or invalid user');
    }
  }
  

}
