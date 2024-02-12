import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FriendsService {
  private apiUrl = `http://localhost:8000/api`;

  constructor(private http: HttpClient) { }

  getUsers(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/allUsers`);
  }

  sendFriendRequest(fromUserId: number, toUserId: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/friend-requests/`, { from_user: fromUserId, to_user: toUserId });
  }
  getPendingRequests(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/pending-requests/`);
  }

  getUserName(id:any): Observable<any>{
    return this.http.get<any>(`${this.apiUrl}/allUsers/${id}`);
  }

  acceptFriendRequest(fromUserId: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/accept-friend-request/`, { from_user_id: fromUserId });
  }

  getFriendList(): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/friend_list/`);
  }

  rejectFriendRequest(fromUserId: number): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/reject-friend-request/`, { from_user_id: fromUserId });
  }

  unfriendByUsername(friendUsername: string): Observable<any> {
    const url = `${this.apiUrl}/unfriend/`;
    return this.http.post<any>(url, { friend_username: friendUsername });
  }

  reportPost(username: string, content: string, reason: string,postUser: string): Observable<any> {
    const reportData = { username, content, reason, postUser};
    return this.http.post<any>(`${this.apiUrl}/report-post/`, reportData);
  }

}
