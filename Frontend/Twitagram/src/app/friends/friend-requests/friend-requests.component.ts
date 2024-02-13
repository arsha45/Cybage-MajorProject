import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { FriendsService } from '../friends.service';
import { PostService } from 'src/app/post/post.service';
import { ToastrService } from 'ngx-toastr';

@Component({
  selector: 'app-friend-requests',
  templateUrl: './friend-requests.component.html',
  styleUrls: ['./friend-requests.component.css']
})
export class FriendRequestsComponent implements OnInit {
  pendingRequests: any[] = [];
  userData: any[] = [];
  currentUserId: number = parseInt(localStorage.getItem('currentUserId') || '0');

  constructor(private postService: PostService , private friendService: FriendsService, private router:Router, private toaster: ToastrService) { }

  ngOnInit(): void {
    this.getPendingRequests();
  }

  getPendingRequests(): void {
    this.friendService.getPendingRequests().subscribe(
      (response: any) => {
        this.pendingRequests = response.results;
        // Fetch user data for each pending request
        this.pendingRequests.forEach(request => {
          this.friendService.getUserName(request.from_user).subscribe(
            (userData: any) => {
              this.userData.push(userData);
            },
            (error: any) => {
              console.error('Error fetching user data:', error);
            }
          );
        });
      },
      (error: any) => {
        console.error('Error fetching pending requests:', error);
      }
    );
  }

  acceptFriendRequest(fromUserId: number): void {
    this.friendService.acceptFriendRequest(fromUserId).subscribe(
      (friend: any) => {
        this.toaster.success(`You accept the friend request`)
        this.router.navigate(['/friend-list'])
      },
      (error: any) => {
        this.toaster.error('Error accepting friend request:', error)
      }
    );
  }

  rejectFriendRequest(fromUserId: number): void {
    this.friendService.rejectFriendRequest(fromUserId).subscribe(
      () => {
        
        this.toaster.success(`You rejected the friend request`)
      },
      (error: any) => {
        this.toaster.error('Error rejecting friend request:', error)
      }
    );
  }

  
  followOrUnfollowUser(post: any): void {
    this.postService.followUser(post).subscribe(
      (data) => {
        console.log('(Un)Follow operation successful:', data);
        this.ngOnInit();
    },
      (error) => {
        console.error('There was an error following the user:', error);
      }
    );
  }

}
