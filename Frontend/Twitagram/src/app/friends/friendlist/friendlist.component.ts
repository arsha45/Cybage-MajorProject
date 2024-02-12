import { Component, OnInit } from '@angular/core';
import { FriendsService } from '../friends.service';

@Component({
  selector: 'app-friendlist',
  templateUrl: './friendlist.component.html',
  styleUrls: ['./friendlist.component.css']
})
export class FriendlistComponent implements OnInit {
  friendList: any[] = [];

  constructor(private friendService: FriendsService) { }

  ngOnInit(): void {
    this.getFriendList();
  }

  getFriendList(): void {
    this.friendService.getFriendList()
      .subscribe(response => {
        console.log(response);
        this.friendList = response.results;
      });
  }

  unfriendByUsername(friendUsername: string): void {
    const confirmed = confirm(`Are you sure you want to unfriend ${friendUsername}?`);
    if (confirmed) {
      this.friendService.unfriendByUsername(friendUsername).subscribe(
        () => {
          console.log('Friend unfriended successfully');
          this.friendList = this.friendList.filter(friend => friend !== friendUsername);
        },
        (error: any) => {
          console.error('Error unfriending friend:', error);
        }
      );
    } else {
      console.log('Unfriend operation cancelled');
    }
  }

}
